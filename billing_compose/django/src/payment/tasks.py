from datetime import datetime

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.shortcuts import redirect
from payments import PaymentStatus, get_payment_model

from config import settings
from payment.models import ItemsToUsers, Payment, Price
from payment.models import User
from payment.utils.utils import get_json_from_permissions

logger = get_task_logger(__name__)


@shared_task(autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 3})
def update_user_info(user_id):
    user = User.objects.get(id=user_id)
    data = {'permissions': get_json_from_permissions(user.items.all())}
    return requests.patch(f"{settings.AUTH_URL}/api/v1/users/{user_id}", data=data)


@shared_task
def check_not_paid_task() -> None:
    for payment in Payment.objects.filter(paid__isnull=True):
        logger.info(
            f'Send notification to user({payment.user_id}) for continue to pay his subscription')


@shared_task
def remove_not_paid_task() -> None:
    result = Payment.objects.filter(status=PaymentStatus.WAITING).delete()
    logger.info(f'removed {result} objects')


@shared_task
def auto_pay() -> None:
    logger.info('### AUTO PAY! ###')
    items_to_users = ItemsToUsers.objects.filter(expires__date=datetime.today())
    logger.info(f'items_to_users: {items_to_users}')
    for items_to_user in items_to_users:
        item_id = items_to_user.item_id
        user_id = items_to_user.user_id
        # create_payment
        payment_model = get_payment_model()
        payment = payment_model.objects.create(
            variant='yookassa',
            user_id=user_id,
            currency=Price.objects.get(item_id=item_id).currency,
            description='Subscription',
            total=Price.objects.get(item_id=item_id).value,
        )
        payment.items.add(items_to_user.item_id)
        return redirect('payment_details', payment_id=payment.id)

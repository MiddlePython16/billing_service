from datetime import datetime
from http import HTTPStatus

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from config import settings
from django.db.models import Q
from payment.models import Item, ItemsToUsers, Payment, User
from payment.utils.utils import get_json_from_permissions
from payments import PaymentStatus, get_payment_model

logger = get_task_logger(__name__)


@shared_task(autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 3})
def update_user_info(user_id):
    user = User.objects.get(id=user_id)
    data = {'permissions': get_json_from_permissions(user.items.all())}
    response = requests.patch(f'{settings.AUTH_URL}/api/v1/users/{user_id}', data=data)
    if response.status_code > HTTPStatus.MULTIPLE_CHOICES:
        logger.info(f'Error while updating user info, status code={response.status_code}')
        raise Exception(f'Error while updating user info, status code={response.status_code}')


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
def remove_not_renewable_expired_items():
    ItemsToUsers.objects.filter(expires__lt=datetime.now(), renewable=False).delete()


@shared_task(autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 1})
def renew_item(item_id, user_id):
    payment_model = get_payment_model()
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id=user_id)
    last_payment = payment_model.objects \
        .filter(Q(user_id=user), Q(items__in=[item])) \
        .prefetch_related('items') \
        .order_by('-created') \
        .first()
    payment = payment_model.objects.create(
        variant=last_payment.variant,
        user_id=user,
        currency=last_payment.currency,
        description='Subscription',
        total=item.prices.get(currency=last_payment.currency).value,
    )
    payment.items.add(item)
    payment.save()
    payment.proceed_auto_payment()


@shared_task
def auto_pay() -> None:
    logger.info('### AUTO PAY! ###')
    items_to_users = ItemsToUsers.objects. \
        filter(expires__lt=datetime.now(), renewable=True). \
        select_related('item_id', 'user_id')
    logger.info(f'items_to_users: {items_to_users}')
    for items_to_user in items_to_users:
        item_id = items_to_user.item_id.id
        user_id = items_to_user.user_id.id
        renew_item.delay(item_id, user_id)

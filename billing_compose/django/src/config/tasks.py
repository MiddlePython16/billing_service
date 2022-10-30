import requests
from celery import shared_task

from config import settings
from payment.models import User
from payment.utils.utils import get_json_from_permissions


@shared_task(autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 3})
def update_user_info(user_id):
    user = User.objects.get(id=user_id)
    data = {'permissions': get_json_from_permissions(user.items.all())}
    return requests.patch(f"{settings.AUTH_URL}/api/v1/users/{user_id}", data=data)

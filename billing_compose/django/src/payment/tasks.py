from celery import shared_task
from celery.utils.log import get_task_logger

from payment.models import Payment

logger = get_task_logger(__name__)


@shared_task
def test_task():
    return 'Ok!'


@shared_task
def check_not_paid_task() -> None:
    for payment in Payment.objects.filter(paid__isnull=True):
        logger.info(
            f'Send notification to user({payment .user_id}) for continue to pay his subscription')


@shared_task
def remove_not_paid_task() -> None:
    Payment.objects.filter(paid__isnull=True).delete()

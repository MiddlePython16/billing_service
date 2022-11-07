import json
import logging

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from payments import PaymentStatus
from payments.signals import status_changed

from config import settings
from payment.kafka import get_kafka_producer
from payment.models import ItemsToUsers
from payment.tasks import update_user_info

logger = logging.getLogger(__name__)


@receiver(status_changed)
def on_status_changed(sender, instance, **kwargs):
    if instance.status == PaymentStatus.CONFIRMED:
        for item in instance.items.all():
            try:
                items_to_users = ItemsToUsers.objects.get(item_id=item, user_id=instance.user_id)
            except ObjectDoesNotExist as e:
                logger.info(e)
                ItemsToUsers.objects.create(item_id=item, user_id=instance.user_id)
            else:
                items_to_users.expires += relativedelta(months=items_to_users.item_id.length)
                items_to_users.save()


@receiver(post_delete, sender=ItemsToUsers)
@receiver(post_save, sender=ItemsToUsers)
def on_item_to_user_create_delete(sender, instance, *args, **kwargs):
    return update_user_info.apply_async((instance.user_id.id,), countdown=5)


@receiver(post_save, sender=ItemsToUsers)
def on_subcription_added(sender, instance, *args, **kwargs):
    kafka_producer = get_kafka_producer()
    if kafka_producer.bootstrap_connected():
        key = f'{instance.user_id.id}+{instance.item_id.id}'.encode('utf-8')
        value = json.dumps({'user_id': str(instance.user_id.id),
                            'item_name': str(instance.item_id.name)}).encode('utf-8')
        kafka_producer.send(topic=settings.SUBSCRIPTION_ADDED_TOPIC,
                            key=key,
                            value=value)

import json

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from payments.signals import status_changed

from config import settings
from payment.kafka import get_kafka_producer
from payment.models import ItemsToUsers
from tasks import update_user_info


@receiver(status_changed)
def on_status_changed(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        for item in instance.items.all():
            ItemsToUsers.objects.create(item_id=item, user_id=instance.user_id)


@receiver(post_delete, sender=ItemsToUsers)
@receiver(post_save, sender=ItemsToUsers)
def on_item_tu_user_create_delete(sender, instance, *args, **kwargs):
    return update_user_info.delay(user_id=instance.user_id.id)


@receiver(post_save, sender=ItemsToUsers)
def on_subcription_added(sender, instance, *args, **kwargs):
    kafka_producer = get_kafka_producer()
    if kafka_producer.bootstrap_connected():
        key = f"{instance.user_id.id}+{instance.item_id}".encode('utf-8')
        value = json.dumps({'user_id': instance.user_id.id,
                            'item_name': instance.item_id.name}).encode('utf-8')
        kafka_producer.send(topic=settings.SUBSCRIPTION_ADDED_TOPIC,
                            key=key,
                            value=value)

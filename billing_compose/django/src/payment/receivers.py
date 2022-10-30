from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from payments.signals import status_changed

from config.tasks import update_user_info
from payment.models import ItemsToUsers


@receiver(status_changed)
def on_status_changed(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        for item in instance.items.all():
            ItemsToUsers.objects.create(item_id=item, user_id=instance.user_id)


@receiver(post_delete, sender=ItemsToUsers)
@receiver(post_save, sender=ItemsToUsers)
def on_item_tu_user_create_delete(sender, instance, *args, **kwargs):
    return update_user_info.delay(user_id=instance.user_id.id)

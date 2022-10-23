import uuid
from decimal import Decimal
from typing import Iterable

from config import settings
from django.db import models
from payments import PurchasedItem
from payments.models import BasePayment
from django.utils.translation import gettext_lazy as _


class Payment(BasePayment):
    def get_failure_url(self) -> str:
        return f'http://example.com/payments/{self.pk}/failure'

    def get_success_url(self) -> str:
        return f'http://example.com/payments/{self.pk}/success'

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # todo стоит переписать
        yield PurchasedItem(
            name='Subscription',
            sku='sbs',
            quantity=1,
            price=Decimal(settings.MONTH_SUBSCRIPTION_PRICE),
            currency='RUB',
        )


class Currencies(models.TextChoices):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), auto_now_add=True)

    class Meta:
        abstract = True


class Item(UUIDMixin):
    expirable = models.BooleanField(_('expirable'))
    length = models.IntegerField(_('length'))

    class Meta:
        db_table = 'billing\".\"items'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


class ItemsToPayments(CreatedMixin):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    payment_id = models.ForeignKey('Payment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing\".\"items_to_payments'


class Permission(UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    json_data = models.JSONField(_('json_data'))

    class Meta:
        db_table = 'billing\".\"permissions'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')


class BillingPayment(UUIDMixin):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing\".\"payments'


class PermissionsToItems(models.Model):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    permission_id = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing\".\"permission_to_items'


class User(UUIDMixin):
    class Meta:
        db_table = 'billing\".\"users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class ItemsToUsers(CreatedMixin, ModifiedMixin):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    expires = models.DateTimeField()

    class Meta:
        db_table = 'billing\".\"items_to_users'


class PricesToItems(models.Model):
    currency = models.TextField(_('currency'), choices=Currencies.choices)
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    value = models.DecimalField()

    class Meta:
        db_table = 'billing\".\"prices_to_items'

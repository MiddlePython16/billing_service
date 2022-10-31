import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Iterable
from urllib.parse import urljoin

from dateutil.relativedelta import relativedelta
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from payments import PurchasedItem
from payments.core import get_base_url, provider_factory
from payments.models import BasePayment


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Currencies(models.TextChoices):
    RUB = 'RUB', 'RUB'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    CNY = 'CNY', 'CNY'


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class ItemsToPayments(CreatedMixin):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    payment_id = models.ForeignKey('Payment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing\".\"items_to_payments'
        constraints = [models.UniqueConstraint(
            fields=['item_id', 'payment_id'],
            name='item_payment_idx')]


class PermissionsToItems(UUIDMixin):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    permission_id = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing\".\"permission_to_items'
        constraints = [models.UniqueConstraint(
            fields=['item_id', 'permission_id'],
            name='item_permission_idx')]


class ItemsToUsers(CreatedMixin, ModifiedMixin, UUIDMixin):
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    expires = models.DateTimeField(blank=True)
    renewable = models.BooleanField(_('renewable'), blank=True)

    class Meta:
        db_table = 'billing\".\"items_to_users'
        constraints = [models.UniqueConstraint(
            fields=['item_id', 'user_id'],
            name='item_user_idx')]

    def save(self, *args, **kwargs):
        if self.expires is None and self.item_id.expirable:
            self.expires = datetime.now(timezone.utc) + relativedelta(months=self.item_id.length)
        self.renewable = self.expires is not None

        return super().save(*args, **kwargs)


class Price(UUIDMixin):
    currency = models.TextField(_('currency'), choices=Currencies.choices)
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='prices')
    value = models.DecimalField(_('value'), max_digits=9, decimal_places=2, default='0.0')

    class Meta:
        db_table = 'billing\".\"prices_to_items'
        verbose_name = _('Prices to items')
        verbose_name_plural = _('Prices to items')
        constraints = [models.UniqueConstraint(
            fields=['item_id', 'currency'],
            name='item_price_currency_idx')]

    def __str__(self):
        return self.currency


class Permission(UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    json_data = models.JSONField(_('json_data'))

    class Meta:
        db_table = 'billing\".\"permissions'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')

    def __str__(self):
        return self.name


class Item(UUIDMixin):
    expirable = models.BooleanField(_('expirable'), default=False)
    name = models.CharField(_('name'), max_length=255)
    length = models.IntegerField(_('length'))
    permissions = models.ManyToManyField(Permission, through='PermissionsToItems')

    class Meta:
        db_table = 'billing\".\"items'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.name


class User(UUIDMixin):
    items = models.ManyToManyField(Item, through='ItemsToUsers')
    payment_method_id = models.UUIDField(blank=True, null=True)

    class Meta:
        db_table = 'billing\".\"users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Payment(BasePayment, UUIDMixin):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    currency = models.TextField(_('currency'), choices=Currencies.choices)
    items = models.ManyToManyField(Item, through='ItemsToPayments')

    def get_failure_url(self) -> str:
        return urljoin(get_base_url(), reverse('payment_failure'))

    def get_success_url(self) -> str:
        return urljoin(get_base_url(), reverse('payment_success'))

    def proceed_auto_payment(self, data=None):
        provider = provider_factory(self.variant, self)
        return provider.proceed_auto_payment(self, data=data)

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # todo стоит переписать
        yield PurchasedItem(
            name='Subscription',
            sku='sbs',
            quantity=1,
            price=Decimal(1),
            currency='RUB',
        )

    class Meta:
        db_table = 'billing\".\"payments'

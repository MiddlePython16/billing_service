from decimal import Decimal
from typing import Iterable

from config import settings
from payments import PurchasedItem
from payments.models import BasePayment


class Payment(BasePayment):
    def get_failure_url(self) -> str:
        return f'http://example.com/payments/{self.pk}/failure'

    def get_success_url(self) -> str:
        return f'http://example.com/payments/{self.pk}/success'

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # Return items that will be included in this payment.
        yield PurchasedItem(
            name='Subscription',
            sku='sbs',
            quantity=1,
            price=Decimal(settings.MONTH_SUBSCRIPTION_PRICE),
            currency='RUB',
        )

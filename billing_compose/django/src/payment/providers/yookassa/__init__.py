import json
import uuid
from urllib.parse import urljoin

from config.settings import logger
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from payment.models import Payment
from payments import PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url
from payments.models import BasePayment
from yookassa import Configuration
from yookassa import Payment as YookassaPayment
from yookassa import Refund
from yookassa.domain.notification import WebhookNotification
from yookassa.domain.response import PaymentResponse


class YookassaProvider(BasicProvider):
    def __init__(self, account_id: str, secret_key: str, **kwargs):

        Configuration.account_id = account_id
        Configuration.secret_key = secret_key

        super().__init__(**kwargs)

    def _create_payment(self, payment: Payment) -> PaymentResponse:
        payment_method_id = payment.user_id.payment_method_id
        payment_params = {
            'amount': {
                'value': str(payment.total),
                'currency': payment.currency,
            },
            'capture': True,
            'description': payment.description,
            'metadata': {
                'token': payment.token,
            },
            'save_payment_method': True,
        }

        if payment_method_id:
            payment_params['payment_method_id'] = payment_method_id
        else:
            payment_params['confirmation'] = {'type': 'redirect',
                                              'return_url': urljoin(get_base_url(), reverse('index')),
                                              },

        confirmation_needed_flag = not bool(payment_method_id)
        return YookassaPayment.create(payment_params, uuid.uuid4()), confirmation_needed_flag

    def get_form(self, payment: BasePayment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment_data, confirmation_needed_flag = self._create_payment(payment)
            payment.transaction_id = payment_data.id
            payment.save()
            if confirmation_needed_flag:
                raise RedirectNeeded(payment_data.confirmation.confirmation_url)
            raise RedirectNeeded(urljoin(get_base_url(), reverse('index')))

    def proceed_auto_payment(self, payment: BasePayment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment_data, confirmation_needed_flag = self._create_payment(payment)
            payment.transaction_id = payment_data.id
            payment.save()

    def get_token_from_request(self, payment: BasePayment, request: HttpRequest):
        payload = json.loads(request.body)
        notification_object = WebhookNotification(payload)
        current_payment = notification_object.object
        return current_payment.metadata.get('token')

    def process_data(self, payment: BasePayment, request: HttpRequest):
        payload = json.loads(request.body)
        try:
            notification_object = WebhookNotification(payload)
        except Exception as error:
            logger.exception(error)

        current_event = notification_object.event
        current_payment = notification_object.object

        if current_event == 'payment.succeeded' and current_payment.amount.value == payment.total:
            payment.captured_amount = current_payment.amount.value
            payment.save()
            payment.change_status(PaymentStatus.CONFIRMED)
            if current_payment.payment_method.saved:
                payment_method_id = payment.user_id.payment_method_id
                if not payment_method_id:
                    user = payment.user_id
                    user.payment_method_id = current_payment.payment_method.id
                    user.save()

        if current_event == 'payment.canceled':
            payment.change_status(PaymentStatus.REJECTED)

        return HttpResponse(status=200)

    def refund(self, payment: BasePayment, amount: int = None) -> int:
        amount = int(amount or payment.total)
        try:
            refund = Refund.create({
                'amount': {
                    'value': amount,
                    'currency': payment.currency,
                },
                'payment_id': payment.transaction_id,
            })
        except Exception as error:
            logger.exception(error)
        else:
            logger.info('[refund]:', refund.json())
            if refund.status != 'succeeded':
                amount = 0
        return amount

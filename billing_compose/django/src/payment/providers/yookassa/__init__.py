import json
import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from payments import PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url
from payments.models import BasePayment

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification


class YookassaProvider(BasicProvider):
    def __init__(self, account_id: str, secret_key: str, **kwargs):

        Configuration.account_id = account_id
        Configuration.secret_key = secret_key

        super().__init__(**kwargs)

    def _create_payment(self, payment: BasePayment) -> Payment:
        return Payment.create({
            "amount": {
                "value": str(payment.total),
                "currency": payment.currency,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": get_base_url(),
            },
            "capture": True,
            "description": payment.description,
            "metadata": {
                'token': payment.token
            }
        }, uuid.uuid4())

    def get_form(self, payment: BasePayment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment_data = self._create_payment(payment)
            raise RedirectNeeded(payment_data.confirmation.confirmation_url)

    def get_token_from_request(self, payment: BasePayment, request: HttpRequest):
        payload = json.loads(request.body)
        notification_object = WebhookNotification(payload)
        current_payment = notification_object.object
        return current_payment.metadata['token']

    def process_data(self, payment: BasePayment, request: HttpRequest):
        payload = json.loads(request.body)
        try:
            notification_object = WebhookNotification(payload)
        except Exception as e:
            print(e)

        current_event = notification_object.event
        # current_payment = notification_object.object

        print('[process_data]:', current_event)

        if current_event == 'payment.succeeded':
            payment.change_status(PaymentStatus.CONFIRMED)

        if current_event == 'payment.canceled':
            payment.change_status(PaymentStatus.REJECTED)

        return HttpResponse(status=200)

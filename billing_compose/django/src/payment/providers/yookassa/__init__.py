import json
import uuid

from django.shortcuts import redirect
from payments import PaymentStatus, RedirectNeeded
from payments.core import BasicProvider

import yookassa


class YookassaProvider(BasicProvider):
    def __init__(self, account_id, secret_key, **kwargs):

        yookassa.Configuration.account_id = account_id
        yookassa.Configuration.secret_key = secret_key

        super().__init__(**kwargs)

    def _create_payment(self, payment) -> yookassa.Payment:
        return yookassa.Payment.create({
            "amount": {
                "value": str(payment.total),
                "currency": payment.currency,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://2055-5-18-159-183.eu.ngrok.io/return_url"
            },
            "capture": True,
            "description": payment.description
        }, uuid.uuid4())

    def get_form(self, payment, data=None):
        payment_data = self._create_payment(payment)
        redirect_to = payment_data.confirmation.confirmation_url

        payment.change_status(PaymentStatus.WAITING)
        raise RedirectNeeded(redirect_to)

    def process_data(self, payment, request):
        payload = json.loads(request.body)
        try:
            notification_object = yookassa.domain.notification.WebhookNotification(payload)
        except Exception as e:
            print(e)

        current_event = notification_object.event
        current_payment = notification_object.object

        if current_event == 'payment.succeeded':
            payment.change_status(PaymentStatus.CONFIRMED)
            return redirect(payment.get_success_url())

        if current_event == 'payment.canceled':
            payment.change_status(PaymentStatus.REJECTED)
            return redirect(payment.get_failure_url())

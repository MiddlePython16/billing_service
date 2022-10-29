import json
import uuid
from xml.etree.ElementTree import QName

from django.http import HttpRequest, HttpResponse
from payment.models import Payment, User
from payments import PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url
from payments.models import BasePayment

from yookassa import Configuration
from yookassa import Payment as YookassaPayment
from yookassa.domain.notification import WebhookNotification
from yookassa.domain.response import PaymentResponse


class YookassaProvider(BasicProvider):
    def __init__(self, account_id: str, secret_key: str, **kwargs):

        Configuration.account_id = account_id
        Configuration.secret_key = secret_key

        super().__init__(**kwargs)

    def _create_payment(self, payment: Payment) -> PaymentResponse:
        payment_method_id = User.objects.get(id=payment.user_id.id).payment_method_id
        if payment_method_id:
            params = {
                "amount": {
                    "value": str(payment.total),
                    "currency": payment.currency,
                },
                "capture": True,
                "payment_method_id": payment_method_id,
                "description": payment.description,
                "metadata": {
                    'token': payment.token
                },
                "save_payment_method": True
            }
            confirmation_needed_flag = False
        else:
            params = {
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
                },
                "save_payment_method": True
            }
            confirmation_needed_flag = True
        return (YookassaPayment.create(params, uuid.uuid4()), confirmation_needed_flag)

    def get_form(self, payment: BasePayment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment_data, confirmation_needed_flag = self._create_payment(payment)
            print('[get_form]:', payment_data.json())
            if confirmation_needed_flag:
                raise RedirectNeeded(payment_data.confirmation.confirmation_url)
            else:
                raise RedirectNeeded(get_base_url())

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
        current_payment = notification_object.object

        print('[process_data]:', current_event)

        if current_event == 'payment.succeeded':
            payment.change_status(PaymentStatus.CONFIRMED)
            if current_payment.payment_method.saved == True:
                payment_method_id = User.objects.get(id=payment.user_id.id).payment_method_id
                print('[process_data]:', current_payment.json())
                if not payment_method_id:
                    user = User.objects.get(id=payment.user_id.id)
                    user.payment_method_id = current_payment.payment_method.id
                    user.save()

        if current_event == 'payment.canceled':
            payment.change_status(PaymentStatus.REJECTED)

        return HttpResponse(status=200)

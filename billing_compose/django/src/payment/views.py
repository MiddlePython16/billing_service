import json
import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from extensions.jwt.jwt import jwt_required

from payment.models import Payment, Product
from payment.tasks import test_task


def payment(request: WSGIRequest) -> HttpResponse:
    test_task.delay()
    return HttpResponse('payment')


@jwt_required(optional=True)
def test(request, *args, **kwargs):
    if kwargs['current_user']:
        return HttpResponse(json.dumps(kwargs['current_user']))
    else:
        return HttpResponse('no user')


def add_test_product(request: WSGIRequest) -> HttpResponse:
    product = Product(user_id='base', description='1 month',
                      price=199, period=1)
    product.save()
    return HttpResponse('')


def add_test_not_paid_payment(request: WSGIRequest) -> HttpResponse:
    product = Product.objects.get()
    payment = Payment(user_id=uuid.uuid4(), product_id=product)
    payment.save()
    return HttpResponse('')


def add_test_paid_payment(request: WSGIRequest) -> HttpResponse:
    product = Product.objects.get()
    payment = Payment(user_id=uuid.uuid4(), product_id=product, paid=datetime.now(
    ), expire_date=datetime.now() + relativedelta(months=product.period))
    payment.save()
    return HttpResponse('')

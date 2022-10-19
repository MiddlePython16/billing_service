import json

from django.http import HttpResponse, JsonResponse

from extensions.jwt.jwt import jwt_required
from payment.tasks import test_task
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
import stripe
from http import HTTPStatus


def payment(request):
    test_task.delay()
    return HttpResponse('payment')


def index(request):
    return render(request, 'index.html')


def thanks(request):
    return render(request, 'thanks.html')


@jwt_required(optional=True)
def test(request, *args, **kwargs):
    if kwargs['current_user']:
        return HttpResponse(json.dumps(kwargs['current_user']))
    else:
        return HttpResponse('no user')


@csrf_exempt
def checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': settings.STRIPE_PRODUCT_PRICE_ID,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('index')),
    )

    return JsonResponse({
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@csrf_exempt
def stripe_webhook(request):
    print('WEBHOOK!')
    # todo получить нормальный токен и вынести в .env
    endpoint_secret = 'whsec_Xj8wBk2qiUcjDEmYu5kfKkOrJCJ5UUjW'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=HTTPStatus.OK)

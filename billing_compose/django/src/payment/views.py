from decimal import Decimal

from config import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from payments import RedirectNeeded, get_payment_model


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment},
    )


def index(request):
    return render(request, 'index.html')


def create_payment(request):
    if request.method == 'GET':
        payment_model = get_payment_model()
        payment = payment_model.objects.create(
            variant='stripe',
            description='Subscription',
            total=Decimal(settings.MONTH_SUBSCRIPTION_PRICE),
            currency='RUB',
            # todo добавить юзернейм пользователя
            billing_first_name='Some name',
        )

        return redirect('payment_details', payment_id=payment.id)

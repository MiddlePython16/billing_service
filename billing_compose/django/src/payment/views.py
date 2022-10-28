from decimal import Decimal

from config import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from payments import RedirectNeeded, get_payment_model

from payment.models import Currencies, Item, User


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
            variant='yookassa',
            user_id=User.objects.get(),
            currency=Currencies.RUB,
            description='Subscription',
            total=199.00,
        )
        return redirect('payment_details', payment_id=payment.id)


def payment_success(request):
    return render(request, 'thanks.html')


def payment_failure(request):
    # change on failure.html
    return render(request, 'thanks.html')

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded
from django.shortcuts import render
from decimal import Decimal


def payment_details(request, *args, **kwargs):
    payment_id = kwargs.get('payment_id')
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )


def index(request):
    if request.GET.get('buy_now_btn'):
        print('Кнопка нажата', flush=True)
    return render(request, 'index.html')


def create_payment(request):
    if request.method == 'GET':
        Payment = get_payment_model()
        # todo поставить нормальные данные
        payment = Payment.objects.create(
            variant='stripe',  # this is the variant from PAYMENT_VARIANTS
            description='Book purchase',
            total=Decimal(120),
            tax=Decimal(20),
            currency='USD',
            delivery=Decimal(10),
            billing_first_name='Sherlock',
            billing_last_name='Holmes',
            billing_address_1='221B Baker Street',
            billing_address_2='',
            billing_city='London',
            billing_postcode='NW1 6XE',
            billing_country_code='GB',
            billing_country_area='Greater London',
            customer_ip_address='127.0.0.1',
        )

        print(payment.transaction_id, flush=True)
        return redirect('payment_details', payment_id=payment.id)

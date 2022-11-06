import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from payment.models import Item, Price, User
from payment.utils.utils import get_json_from_permissions
from payments import RedirectNeeded, get_payment_model

logger = logging.getLogger(__name__)


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
    logger.info('get request to index')
    return render(request, 'index.html')


def create_payment(request):
    if request.method == 'GET':
        logger.info('get request create_payments')
        item = Item.objects.get(name='base')

        payment_model = get_payment_model()
        payment = payment_model.objects.create(
            variant='yookassa',
            user_id=User.objects.create(),
            currency=Price.objects.get(item_id=item.id).currency,
            description='Subscription',
            total=Price.objects.get(item_id=item.id).value,
        )
        payment.items.add(item)
        return redirect('payment_details', payment_id=payment.id)


def refund_payment(request, id):
    payment_model = get_payment_model()
    payment = payment_model.objects.get(id=id)
    payment.refund(amount=payment.total)
    return HttpResponse(status=200)


def payment_success(request):
    return render(request, 'thanks.html')


def payment_failure(request):
    # change on failure.html
    return render(request, 'thanks.html')


def get_json_blob(request, user_id):
    user = User.objects.get(id=user_id)
    return HttpResponse(str({'permissions': get_json_from_permissions(user.items.all())}))

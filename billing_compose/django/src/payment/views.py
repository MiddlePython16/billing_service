from django.http import HttpResponse

from payment.tasks import test_task


def payment(request):
    test_task.delay()
    return HttpResponse('payment')

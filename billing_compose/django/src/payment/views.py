import json

from django.http import HttpResponse

from extensions.jwt.jwt import jwt_required
from payment.tasks import test_task


def payment(request):
    test_task.delay()
    return HttpResponse('payment')


@jwt_required(optional=True)
def test(request, *args, **kwargs):
    if kwargs['current_user']:
        return HttpResponse(json.dumps(kwargs['current_user']))
    else:
        return HttpResponse('no user')

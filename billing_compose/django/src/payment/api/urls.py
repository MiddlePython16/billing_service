from django.urls import path, include

urlpatterns = [
    path('v1/', include('payment.api.v1.urls')),
]
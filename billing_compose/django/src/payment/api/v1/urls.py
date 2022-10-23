from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from payment.api.v1.views.payment import PaymentCreateView

urlpatterns = [
    path('payments/', PaymentCreateView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='v1schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='v1schema'), name='swagger'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='v1schema'), name='redoc'),
]
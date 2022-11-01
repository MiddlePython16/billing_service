from django.contrib import admin
from django.urls import include, path
from payment import views

urlpatterns = [
    path('api/', include('payment.api.urls')),

    path('admin/', admin.site.urls),

    path('payments/', include('payments.urls')),

    path('', views.index, name='index'),
    path('payment_details/<str:payment_id>/', views.payment_details, name='payment_details'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('get_json_blob/<str:user_id>', views.get_json_blob, name='get_json_blob'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('refund_payment/<uuid:id>', views.refund_payment, name='refund_payment'),
]

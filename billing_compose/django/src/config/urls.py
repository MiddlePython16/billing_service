"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from payment import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('payments/', include('payments.urls')),

    path('', include('payment.urls')),

    path('', views.index, name='index'),
    path('payment_details/<str:payment_id>/', views.payment_details, name='payment_details'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('get_json_blob/<str:user_id>', views.get_json_blob, name='get_json_blob'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('refund_payment/<uuid:id>', views.refund_payment, name='refund_payment'),

]

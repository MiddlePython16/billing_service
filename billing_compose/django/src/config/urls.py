from django.urls import include, path

urlpatterns = [

    path('billing/', include('payment.urls')),

]

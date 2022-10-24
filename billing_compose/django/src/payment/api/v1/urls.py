from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from payment.api.v1.views import item, payment, permission, user

urlpatterns = [
    path('payments/', payment.PaymentCreateView.as_view()),
    path('payments/', payment.PaymentListView.as_view()),
    path('payments/<uuid:pk>', payment.PaymentRetrieveView.as_view()),
    path('payments/<uuid:pk>', payment.PaymentUpdateView.as_view()),
    path('payments/<uuid:pk>', payment.PaymentDestroyView.as_view()),

    path('items/', item.ItemCreateView.as_view()),
    path('items/', item.ItemListView.as_view()),
    path('items/<uuid:pk>', item.ItemRetrieveView.as_view()),
    path('items/<uuid:pk>', item.ItemUpdateView.as_view()),
    path('items/<uuid:pk>', item.ItemDestroyView.as_view()),

    path('permissions/', permission.PermissionCreateView.as_view()),
    path('permissions/', permission.PermissionListView.as_view()),
    path('permissions/<uuid:pk>', permission.PermissionRetrieveView.as_view()),
    path('permissions/<uuid:pk>', permission.PermissionUpdateView.as_view()),
    path('permissions/<uuid:pk>', permission.PermissionDestroyView.as_view()),

    path('users/', user.UserCreateView.as_view()),
    path('users/', user.UserListView.as_view()),
    path('users/<uuid:pk>', user.UserRetrieveView.as_view()),
    path('users/<uuid:pk>', user.UserUpdateView.as_view()),
    path('users/<uuid:pk>', user.UserDestroyView.as_view()),

    path('schema/', SpectacularAPIView.as_view(), name='v1schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='v1schema'), name='swagger'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='v1schema'), name='redoc'),
]

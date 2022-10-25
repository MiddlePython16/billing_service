from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from payment.api.v1.views import item, payment, permission, user, price
from payment.api.v1.views.item import PermissionToItemViewSet
from payment.api.v1.views.payment import ItemToPaymentViewSet
from payment.api.v1.views.user import ItemToUserViewSet

router = DefaultRouter()
router.register(r'items', item.ItemViewSet, basename='items')
router.register(r'payments', payment.PaymentViewSet, basename='payments')
router.register(r'permissions', permission.PermissionViewSet, basename='permissions')
router.register(r'prices', price.PriceViewSet, basename='prices')
router.register(r'users', user.UserViewSet, basename='users')

users_router = NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'items', ItemToUserViewSet, basename='items_to_users')

items_router = NestedDefaultRouter(router, r'items', lookup='item')
items_router.register(r'permissions', PermissionToItemViewSet, basename='permissions_to_items')

payments_router = NestedDefaultRouter(router, r'payments', lookup='payment')
payments_router.register(r'items', ItemToPaymentViewSet, basename='items_to_payments')

urlpatterns = [
    path('', include(router.urls)),

    path('', include(users_router.urls)),
    path('', include(items_router.urls)),
    path('', include(payments_router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='v1schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='v1schema'), name='swagger'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='v1schema'), name='redoc'),
]

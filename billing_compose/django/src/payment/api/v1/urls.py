from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from payment.api.v1.views import item, payment, permission, price, user
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('items', item.ItemViewSet, basename='items')
router.register('payments', payment.PaymentViewSet, basename='payments')
router.register('permissions', permission.PermissionViewSet, basename='permissions')
router.register('prices', price.PriceViewSet, basename='prices')
router.register('users', user.UserViewSet, basename='users')

users_router = NestedDefaultRouter(router, 'users', lookup='user')
users_router.register('items', user.ItemToUserViewSet, basename='items_to_users')

items_router = NestedDefaultRouter(router, 'items', lookup='item')
items_router.register(
    'permissions',
    item.PermissionToItemViewSet,
    basename='permissions_to_items',
)

payments_router = NestedDefaultRouter(router, 'payments', lookup='payment')
payments_router.register(
    'items',
    payment.ItemToPaymentViewSet,
    basename='items_to_payments',
)

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

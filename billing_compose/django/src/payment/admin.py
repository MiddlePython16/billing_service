from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from payment import models


class PricesToItemsInline(admin.TabularInline):
    model = models.Price
    extra = 0


class PermissionsToItemsInline(admin.TabularInline):
    model = models.PermissionsToItems
    extra = 0


class ItemsToUsersInline(admin.TabularInline):
    model = models.ItemsToUsers
    extra = 0


class ItemsToPaymentsInline(admin.TabularInline):
    model = models.ItemsToPayments
    extra = 0


class PrefetchRelatedMixin:
    list_prefetch_related = ()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(*self.list_prefetch_related)


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin, PrefetchRelatedMixin):
    inlines = (ItemsToPaymentsInline,)

    list_prefetch_related = ('items',)

    search_fields = ('status', 'id')

    list_display = ('id', 'get_items', 'status', 'currency', 'total', 'captured_amount')

    def get_items(self, obj):
        return ', '.join(item.name for item in obj.items.all())  # noqa: WPS110

    get_items.short_description = _('items')  # type: ignore


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin, PrefetchRelatedMixin):
    inlines = (ItemsToUsersInline,)

    list_display = ('id', 'get_items')

    list_prefetch_related = ('items',)

    search_fields = ('id',)

    def get_items(self, obj):
        return ', '.join(item.name for item in obj.items.all())

    get_items.short_description = _('items')  # type: ignore


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin, PrefetchRelatedMixin):
    inlines = (PermissionsToItemsInline, PricesToItemsInline)
    list_prefetch_related = ('permissions', 'prices')
    search_fields = ('id', 'name')


@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name')


@admin.register(models.Price)
class PricesToItemsAdmin(admin.ModelAdmin):
    search_fields = ('currency', 'id')
    list_filter = ('currency',)

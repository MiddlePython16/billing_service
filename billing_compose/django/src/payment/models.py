import uuid

from django.core.validators import MinValueValidator
from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Product(UUIDMixin):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    price = models.DecimalField('price', max_digits=6, decimal_places=2)
    period = models.DecimalField(
        'period', max_digits=2, decimal_places=0, blank=True, validators=[MinValueValidator(1)])


class Payment(UUIDMixin):
    user_id = models.UUIDField('user id')
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DateTimeField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)

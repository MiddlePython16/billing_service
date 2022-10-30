# Generated by Django 4.1.2 on 2022-10-25 08:08

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expirable', models.BooleanField(default=False, verbose_name='expirable')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('length', models.IntegerField(verbose_name='length')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'db_table': 'billing"."items',
            },
        ),
        migrations.CreateModel(
            name='ItemsToPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.item')),
            ],
            options={
                'db_table': 'billing"."items_to_payments',
            },
        ),
        migrations.CreateModel(
            name='ItemsToUsers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('expires', models.DateTimeField()),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.item')),
            ],
            options={
                'db_table': 'billing"."items_to_users',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('json_data', models.JSONField(verbose_name='json_data')),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
                'db_table': 'billing"."permissions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('items', models.ManyToManyField(through='payment.ItemsToUsers', to='payment.item')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'billing"."users',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.TextField(choices=[('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR'), ('CNY', 'CNY')], verbose_name='currency')),
                ('value', models.DecimalField(decimal_places=2, default='0.0', max_digits=9, verbose_name='value')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='payment.item')),
            ],
            options={
                'verbose_name': 'Prices to items',
                'verbose_name_plural': 'Prices to items',
                'db_table': 'billing"."prices_to_items',
            },
        ),
        migrations.CreateModel(
            name='PermissionsToItems',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.item')),
                ('permission_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.permission')),
            ],
            options={
                'db_table': 'billing"."permission_to_items',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('variant', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('waiting', 'Waiting for confirmation'), ('preauth', 'Pre-authorized'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('refunded', 'Refunded'), ('error', 'Error'), ('input', 'Input')], default='waiting', max_length=10)),
                ('fraud_status', models.CharField(choices=[('unknown', 'Unknown'), ('accept', 'Passed'), ('reject', 'Rejected'), ('review', 'Review')], default='unknown', max_length=10, verbose_name='fraud check')),
                ('fraud_message', models.TextField(blank=True, default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255)),
                ('total', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('delivery', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('description', models.TextField(blank=True, default='')),
                ('billing_first_name', models.CharField(blank=True, max_length=256)),
                ('billing_last_name', models.CharField(blank=True, max_length=256)),
                ('billing_address_1', models.CharField(blank=True, max_length=256)),
                ('billing_address_2', models.CharField(blank=True, max_length=256)),
                ('billing_city', models.CharField(blank=True, max_length=256)),
                ('billing_postcode', models.CharField(blank=True, max_length=256)),
                ('billing_country_code', models.CharField(blank=True, max_length=2)),
                ('billing_country_area', models.CharField(blank=True, max_length=256)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('billing_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('customer_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('message', models.TextField(blank=True, default='')),
                ('token', models.CharField(blank=True, default='', max_length=36)),
                ('captured_amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.TextField(choices=[('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR'), ('CNY', 'CNY')], verbose_name='currency')),
                ('items', models.ManyToManyField(through='payment.ItemsToPayments', to='payment.item')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.user')),
            ],
            options={
                'db_table': 'billing"."payments',
            },
        ),
        migrations.AddField(
            model_name='itemstousers',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.user'),
        ),
        migrations.AddField(
            model_name='itemstopayments',
            name='payment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.payment'),
        ),
        migrations.AddField(
            model_name='item',
            name='permissions',
            field=models.ManyToManyField(through='payment.PermissionsToItems', to='payment.permission'),
        ),
    ]

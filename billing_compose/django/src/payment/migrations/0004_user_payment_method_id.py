# Generated by Django 4.1.2 on 2022-10-29 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_itemstousers_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='payment_method_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]

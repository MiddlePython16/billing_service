# Generated by Django 4.1.2 on 2022-10-31 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_rename_payments_rel'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemstousers',
            name='renewable',
            field=models.BooleanField(blank=True, default=None, verbose_name='renewable'),
            preserve_default=False,
        ),
    ]
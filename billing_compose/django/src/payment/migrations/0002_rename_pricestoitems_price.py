# Generated by Django 4.1.2 on 2022-10-24 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PricesToItems',
            new_name='Price',
        ),
    ]
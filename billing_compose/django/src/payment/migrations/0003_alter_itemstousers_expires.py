# Generated by Django 4.1.2 on 2022-10-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_constraints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemstousers',
            name='expires',
            field=models.DateTimeField(blank=True),
        ),
    ]

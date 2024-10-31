# Generated by Django 5.1.1 on 2024-10-31 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_restaurant_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

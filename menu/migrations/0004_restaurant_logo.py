# Generated by Django 5.1.1 on 2024-10-29 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_restaurant_address_alter_restaurant_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='restaurant_photos/'),
        ),
    ]

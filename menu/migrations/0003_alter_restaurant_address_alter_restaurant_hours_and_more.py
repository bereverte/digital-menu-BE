# Generated by Django 5.1.1 on 2024-10-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menuitem_options_alter_restaurantuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='hours',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

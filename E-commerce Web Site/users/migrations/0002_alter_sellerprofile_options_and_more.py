# Generated by Django 5.0.6 on 2024-06-26 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sellerprofile',
            options={'verbose_name_plural': 'seller_profile'},
        ),
        migrations.AlterModelTable(
            name='sellerprofile',
            table='seller_profile',
        ),
    ]
# Generated by Django 5.0.6 on 2024-06-20 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0007_watchlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchlist',
            options={'verbose_name_plural': 'watchlist'},
        ),
        migrations.AlterModelTable(
            name='watchlist',
            table='watchlist',
        ),
    ]

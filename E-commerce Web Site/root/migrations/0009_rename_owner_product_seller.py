# Generated by Django 5.0.6 on 2024-06-26 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0008_alter_watchlist_options_alter_watchlist_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='owner',
            new_name='seller',
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-26 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0010_alter_product_seller'),
        ('users', '0002_alter_sellerprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sellerprofile'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_birth_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_year',
            field=models.DateField(null=True),
        ),
    ]
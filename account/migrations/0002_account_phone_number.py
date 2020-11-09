# Generated by Django 3.1.1 on 2020-11-09 20:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='1234567890', max_length=128, region=None),
        ),
    ]
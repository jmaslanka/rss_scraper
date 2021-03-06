# Generated by Django 2.2.10 on 2020-02-12 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('JPY', 'JPY'), ('BGN', 'BGN'), ('CZK', 'CZK'), ('DKK', 'DKK'), ('EEK', 'EEK'), ('GBP', 'GBP'), ('HUF', 'HUF'), ('PLN', 'PLN'), ('RON', 'RON'), ('SEK', 'SEK'), ('CHF', 'CHF'), ('ISK', 'ISK'), ('NOK', 'NOK'), ('HRK', 'HRK'), ('RUB', 'RUB'), ('TRY', 'TRY'), ('AUD', 'AUD'), ('BRL', 'BRL'), ('CAD', 'CAD'), ('CNY', 'CNY'), ('HKD', 'HKD'), ('IDR', 'IDR'), ('INR', 'INR'), ('KRW', 'KRW'), ('MXN', 'MXN'), ('MYR', 'MYR'), ('NZD', 'NZD'), ('PHP', 'PHP'), ('SGD', 'SGD'), ('THB', 'THB'), ('ZAR', 'ZAR')], max_length=3, unique=True, verbose_name='currency')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=14, verbose_name='rate')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Exchange rate',
                'verbose_name_plural': 'Exchange rates',
            },
        ),
    ]

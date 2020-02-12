import pytest
from unittest import mock

import requests
from django.urls import reverse
from django.test import override_settings

from .models import ExchangeRate
from .literals import CURRENCIES


@pytest.mark.django_db
def test_rates_list(client):
    r = client.get(reverse('api:exchangerate-list'))
    assert r.status_code == 200
    assert r.json()['results'] == []

    items_count = 5
    rate = 24.5423
    ExchangeRate.objects.bulk_create([
        ExchangeRate(currency=c[0], rate=rate) for c in CURRENCIES[:items_count]
    ])

    r = client.get(reverse('api:exchangerate-list'))
    assert r.status_code == 200
    assert r.json()['count'] == items_count
    assert r.json()['results'][2]['currency'] == CURRENCIES[2][0]
    assert r.json()['results'][2]['rate'] == '24.542300'


@pytest.mark.django_db
def test_rates_details(client):
    r = client.get(reverse('api:exchangerate-detail', kwargs=dict(currency='USD')))

    assert r.status_code == 404
    assert r.json() == {'detail': 'Not found.'}

    currency = CURRENCIES[0][0]
    rate = 12.11
    ExchangeRate.objects.create(currency=currency, rate=12.110000)

    r = client.get(reverse('api:exchangerate-detail', kwargs=dict(currency=currency)))
    assert r.status_code == 200
    assert r.json()['rate'] == '12.110000'


class TestRatesUpdate:
    def mocked_rates_response(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                rate = 12.2345
                self.ok = True
                self.content = f'<cb:value frequency="daily" decimals="4">{rate}</cb:value>'.encode('UTF-8')
        
        return MockResponse()


    @pytest.mark.django_db
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @mock.patch('requests.get', side_effect=mocked_rates_response)
    def test_rates_update(self, mock, client):
        r = client.get(reverse('api:exchangerate-list'))
        assert r.status_code == 200
        assert r.json()['count'] == 0

        r = client.post(reverse('api:update-rates'))
        assert r.status_code == 200

        r = client.get(reverse('api:exchangerate-list'))
        assert r.status_code == 200
        assert r.json()['count'] == len(CURRENCIES)

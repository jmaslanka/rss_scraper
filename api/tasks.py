from datetime import datetime
from decimal import Decimal
import logging
import re

import requests
from celery import shared_task

from .literals import CURRENCIES
from .models import ExchangeRate


logger = logging.getLogger(__name__)


@shared_task
def update_exchange_rates() -> None:
    BASE_URL = 'https://www.ecb.europa.eu/rss/fxref-XXX.html'
    updated_rates = {}
    objects_to_update = []
    current_time = datetime.now()
    
    for currency in [v[0] for v in CURRENCIES]:
        try:
            response = requests.get(
                BASE_URL.replace('XXX', currency.lower()),
                headers={'user-agent': 'Exchange rates API'},
                timeout=1.5,
            )
            if not response.ok:
                logger.error(f'Updating rate for {currency} failed.')
                continue

            rate = re.search(r'>(\d+\.\d+)<\/cb:value>', str(response.content)).group(1)
        except (requests.RequestException, IndexError, AttributeError):
            logger.exception(f'Updating rate for {currency} failed.')
            continue
        
        updated_rates[currency] = Decimal(rate)

    rates_list = ExchangeRate.objects.filter(currency__in=updated_rates.keys())

    for obj in rates_list:
        obj.rate = updated_rates.pop(obj.currency)
        obj.updated_at = current_time
        objects_to_update.append(obj)

    # Creating those that aren't in the DB
    if updated_rates:
        ExchangeRate.objects.bulk_create([
            ExchangeRate(
                currency=obj[0],
                rate=obj[1],
                updated_at=current_time,
            ) for obj in updated_rates.items()
        ])

    if objects_to_update:
        ExchangeRate.objects.bulk_update(objects_to_update, ['rate', 'updated_at'])

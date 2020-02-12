from django.db import models
from django.utils.translation import gettext_lazy as _

from .literals import CURRENCIES


class ExchangeRate(models.Model):
    """Store exchange rate of given currency to Euro."""

    currency = models.CharField(
        _('currency'),
        choices=CURRENCIES,
        max_length=3,
        unique=True,
    )
    rate = models.DecimalField(
        _('rate'),
        max_digits=14,
        decimal_places=6,
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Exchange rate')
        verbose_name_plural = _('Exchange rates')

    def __str__(self):
        return f'{self.currency} - {self.rate}'

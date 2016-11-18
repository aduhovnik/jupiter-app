from django.db import models
from djmoney.models.fields import MoneyField


def money_field():
    return MoneyField(
        max_digits=15, decimal_places=2, default_currency='BYN'
    )


def percentage_field():
    return models.DecimalField(max_digits=6, decimal_places=3)

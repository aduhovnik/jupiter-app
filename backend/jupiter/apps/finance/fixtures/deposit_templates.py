# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import DepositTemplate


DEPOSIT_TEMPLATES = [
    {
        "name": "Метида",
        "description": "Разместить денежные средства можно на срок 3 месяца. "
                       "Проценты начисляются ежемесячно на текущий счет. "
                       "Фиксированная процентная ставка по вкладу.",
        "percentage": {
            "BYN": {
                "3": 5.0
                },
            "USD": {
                "3": 2.0
            },
            "EUR": {
                "3": 2.0
            }
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "min_amount": 10,
        "max_amount": None,
        "cancellation_condition": DepositTemplate.CLOSING_ANYTIME_WITH_LOSS,
        "prolongation": False,
        "additional_contributions": True,
    },

    {
        "name": "Карпо",
        "description": "Срочный безотзывный банковский вклад.",
        "percentage": {
            "BYN": {
                "24": 8.0,
                "36": 9.0
            },

            "USD": {
                "24": 3.0,
                "36": 3.5,
            },
            "EUR": {
                "24": 3.0,
                "36": 3.5,
            },
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "min_amount": 10,
        "max_amount": None,
        "cancellation_condition": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
    },

    {
        "name": "Фива",
        "description": "Cнятие без потери процентов всей суммы вклада в любое время. "
                       "Проценты начисляются за уже прошедшие полные месяцы.",
        "percentage": {
            "BYN": {
                "3": 5.0,
                "6": 6.0,
                "12": 7.0,
                "36": 8.0,
            },
            "USD": {
                "3": 1.0,
                "6": 1.5,
                "12": 2.0,
                "36": 2.5,
            },
            "EUR": {
                "3": 1.0,
                "6": 1.5,
                "12": 2.0,
                "36": 2.5,
            },
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "min_amount": 10,
        "max_amount": None,
        "cancellation_condition": DepositTemplate.CLOSING_IN_END,
        "prolongation": False,
        "additional_contributions": False,
    },

    {
        "name": "Лида",
        "description": "Срочный безотзывный банковский вклад.",
        "percentage": {
            "BYN": {
                "12": 18,
            },
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "min_amount": 100,
        "max_amount": None,
        "cancellation_condition": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
    },

]

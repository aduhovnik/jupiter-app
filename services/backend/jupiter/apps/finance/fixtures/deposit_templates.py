# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import DepositTemplate


DEPOSIT_TEMPLATES = [
    {
        "name": "Метида",
        "description": "Усовершенствованный сберегательный продукт, представляющий новые "
                       "возможности и преимущества стандартной линейки вкладов",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 5
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 5,
                    }
                ]
            },
            "EUR": {
                "min_amount": 30,
                "max_term": 3,
                "percentage": [
                    {
                        "term": 3,
                        "percentage": 5,
                    }
                ]
            }
        },
        "indexing": DepositTemplate.INDEXING_DAILY,
        "closing": DepositTemplate.CLOSING_ANYTIME_WITH_LOSS,
        "prolongation": False,
        "additional_contributions": True,
    },

    {
        "name": "Карпо",
        "description": "Срочный безотзывный банковский вклад.",
        "currency": {
            "BYN": {
                "min_amount": 200,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 6,
                    },
                    {
                        "term": 24,
                        "percentage": 8,
                    },
                    {
                        "term": 36,
                        "percentage": 10,
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 3
                    },
                    {
                        "term": 24,
                        "percentage": 3.5
                    },
                    {
                        "term": 36,
                        "percentage": 4
                    },
                ]
            },
            "EUR": {
                "min_amount": 70,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 12,
                        "percentage": 3.5
                    },
                    {
                        "term": 24,
                        "percentage": 4
                    },
                    {
                        "term": 36,
                        "percentage": 4.5
                    },
                ]
            }
        },
        "indexing": DepositTemplate.INDEXING_QUARTERLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
    },

    {
        "name": "Фива",
        "description": "Cнятие без потери процентов всей суммы вклада в любое время. "
                       "Проценты начисляются за уже прошедшие полные месяцы.",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 32,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 5,
                    },
                    {
                        "term": 12,
                        "percentage": 6,
                    },
                    {
                        "term": 24,
                        "percentage": 7,
                    },
                    {
                        "term": 36,
                        "percentage": 8,
                    }
                ]
            },
            "USD": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 2.5
                    },
                    {
                        "term": 12,
                        "percentage": 3
                    },
                    {
                        "term": 24,
                        "percentage": 3.5
                    },
                    {
                        "term": 36,
                        "percentage": 4
                    },
                ]
            },
            "EUR": {
                "min_amount": 50,
                "max_term": 36,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 3,
                    },
                    {
                        "term": 12,
                        "percentage": 3.5,
                    },
                    {
                        "term": 24,
                        "percentage": 4,
                    },
                    {
                        "term": 36,
                        "percentage": 4.5,
                    },
                ]
            }
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": False,
        "additional_contributions": False,
    },

    {
        "name": "Лида",
        "description": "Срочный безотзывный банковский вклад.",
        "currency": {
            "BYN": {
                "min_amount": 100,
                "max_term": 18,
                "percentage": [
                    {
                        "term": 6,
                        "percentage": 12,
                    },
                    {
                        "term": 12,
                        "percentage": 14,
                    },
                    {
                        "term": 18,
                        "percentage": 16,
                    }
                ]
            }
        },
        "indexing": DepositTemplate.INDEXING_MONTHLY,
        "closing": DepositTemplate.CLOSING_IN_END,
        "prolongation": True,
        "additional_contributions": False,
    },

]

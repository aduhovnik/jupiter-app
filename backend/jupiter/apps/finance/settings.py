# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import moneyed
from moneyed.localization import _FORMATTER
from decimal import ROUND_HALF_EVEN


BYN = moneyed.add_currency(
    code='BYN',
    numeric='933',
    name='Belarusian ruble',
    countries=('BELARUS', )
)

_FORMATTER.add_sign_definition(
    'default',
    BYN,
    suffix=u'Br'
)

_FORMATTER.add_formatting_definition(
    'by_BY',
    group_size=3, group_separator=".", decimal_point=",",
    positive_sign="",  trailing_positive_sign="",
    negative_sign="-", trailing_negative_sign="",
    rounding_method=ROUND_HALF_EVEN
)


#indexations
YEARLY = 0
DAILY = 1
MONTHLY = 2
QUARTERLY = 3

#concellations
ANYTIME = 0
ANYTIME_WITH_LOSSY = 1
ONLY_AFTER_END = 2

DEPOSIT_TEMPLATES = [
    {
        "name": "Метида",
        "description": "Разместить денежные средства можно на срок 3 месяца. Проценты начисляются ежемесячно на текущий счет. Фиксированная процентная ставка по вкладу.",
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
        "indexing": MONTHLY,
        "min_amount": 10,#BYN
        "max_amount": 0,
        "cancellation_condition": ANYTIME_WITH_LOSSY,
        "prolongation": False,
        "additional_contributions": True,
        # http://www.belinvestbank.by/private-clients/deposits/inostrannoj-valjute/otlichiy/
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
        "indexing": MONTHLY,
        "min_amount": 10,#BYN
        "max_amount": 0,
        "cancellation_condition": ONLY_AFTER_END,
        "prolongation": True,
        "additional_contributions": False,
        # http://www.belinvestbank.by/private-clients/deposits/inostrannoj-valjute/srochii-bezotzivnii-bankovskii-vklad-val/
    },

    {
        "name": "Фива",
        "description": "Cнятие без потери процентов всей суммы вклада в любое время. Проценты начисляются за уже прошедшие полные месяцы.",
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
        "indexing": MONTHLY,
        "min_amount": 10,#BYN
        "max_amount": 0,
        "cancellation_condition": ANYTIME,
        "prolongation": False,
        "additional_contributions": False,
        # http://www.belinvestbank.by/private-clients/deposits/inostrannoj-valjute/srochii-otzivnii-vklad-c-pravom-dosrochnogo-vostrebovania/
    },

    {
        "name": "Лида",
        "description": "Срочный безотзывный банковский вклад.",
        "percentage": {
            "BYN": {
                "12": 18,
            },
        },
        "indexing": MONTHLY,
        "min_amount": 100,#BYN
        "max_amount": 0,
        "cancellation_condition": ONLY_AFTER_END,
        "prolongation": True,
        "additional_contributions": False,
        # http://www.belinvestbank.by/private-clients/deposits/nacionalnoj-valjute/bezotzivnii_nakopitelnii_plus_byr/
    },

]


CREDIT_TEMPLATES = [
    {
        "name": "Европа",
        "description": "Кредитный продукт, на базе которого вы выбираете срок кредитования. Максимальная/минимальная суммы кредита расчитывается на основании платежеспособности клиента, без залога и поручителей.",
        "annual_percentage_rate": 29.2,
        "max_amount": {
            "fixed": 5000.0, #BYN
            "annual_income_mul": 4.1,
            "percent_of_purchase": 0.0,
        },
        "min_amount": {
            "fixed": 1000.0, #BYN
            "annual_income_mul": 0.7,
            "percent_of_purchase": 0.0,
        },
        "max_duration": 5*12,
        "fine_percentage": 0.6,
        "issue_online": False,
        "allowed_methods_of_ensuring": [0]
    },

    {
        "name": "Калисто",
        "description": "Потребительский кредит. Очень удобен, если вам нужна небольшая сумма. Процентная ставка вас приятно удивит.",
        "annual_percentage_rate": 23.7,
        "max_amount": {
            "fixed": 5000, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 0,
        },
        "min_amount": {
            "fixed": 1000, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 0,
        },
        "max_duration": 18,
        "fine_percentage": 0.5,
        "issue_online": False,
        "allowed_methods_of_ensuring": [0]
    },

    {
        "name": "Ио",
        "description": "Потребительский экспресс кредит. Позволяет вам взять кредит онлайн.",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": 5000, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 0,
        },
        "min_amount": {
            "fixed": 500, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 0,
        },
        "max_duration": 12,
        "fine_percentage": 0.7,
        "issue_online": True,
        "allowed_methods_of_ensuring": [0]
    },

    {
        "name": "Адреаста",
        "description": "Кредит на автомобиль. Автоматически переводит деньги на счет продавца."
                       " Как способ обеспечения вы можете выбрать либо залог автомобиля, либо поручительство",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 40,
        },
        "max_duration": 7*12,
        "fine_percentage": 0.3,
        "issue_online": False,
        "allowed_methods_of_ensuring": [1, 2]
    },

    {
        "name": "Ганимед",
        "description": "Кредит на приобретение уже построенной недвижимости. Приобретаемая недвижимость является залогом.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 80,
        },
        "min_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 50,
        },
        "max_duration": 10*12,
        "fine_percentage": 0.25,
        "issue_online": False,
        "allowed_methods_of_ensuring": [1]
    },

    {
        "name": "Ганимед+",
        "description": "Кредит на приобретение строящейся недвижимости. Приобретаемая недвижимость является залогом.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": 0, #BYN
            "annual_income_mul": 0,
            "percent_of_purchase": 30,
        },
        "max_duration": 20*12,
        "fine_percentage": 0.2,
        "issue_online": False,
        "allowed_methods_of_ensuring": [1]
    },

]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from finance.models import CreditTemplate


CREDIT_TEMPLATES = [
    {
        "name": "Европа",
        "description": "Кредитный продукт, на базе которого вы выбираете "
                       "срок кредитования. Максимальная/минимальная суммы "
                       "кредита расчитывается на основании платежеспособности "
                       "клиента, без залога и поручителей.",
        "annual_percentage_rate": 29.2,
        "max_amount": {
            "fixed": 5000.0,
            "annual_income_mul": 4.1,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 1000.0,
            "annual_income_mul": 0.7,
            "percent_of_purchase": None,
        },
        "max_duration": 5*12,
        "fine_percentage": 0.6,
        "issue_online": False,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_FINE
        ]
    },

    {
        "name": "Калисто",
        "description": "Потребительский кредит. Очень удобен, если вам нужна "
                       "небольшая сумма. Процентная ставка вас приятно удивит.",
        "annual_percentage_rate": 23.7,
        "max_amount": {
            "fixed": 5000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 1000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 18,
        "fine_percentage": 0.5,
        "issue_online": False,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_FINE
        ]
    },

    {
        "name": "Ио",
        "description": "Потребительский экспресс кредит. "
                       "Позволяет вам взять кредит онлайн.",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": 5000,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "min_amount": {
            "fixed": 500,
            "annual_income_mul": None,
            "percent_of_purchase": None,
        },
        "max_duration": 12,
        "fine_percentage": 0.7,
        "issue_online": True,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_FINE
        ]
    },

    {
        "name": "Адреаста",
        "description": "Кредит на автомобиль. Автоматически переводит деньги "
                       "на счет продавца. Как способ обеспечения вы можете "
                       "выбрать либо залог автомобиля, либо поручительство",
        "annual_percentage_rate": 33,
        "max_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 40,
        },
        "max_duration": 7 * 12,
        "fine_percentage": 0.3,
        "issue_online": False,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_PLEDGE,
            CreditTemplate.ENSURING_SURETY
        ]
    },

    {
        "name": "Ганимед",
        "description": "Кредит на приобретение уже построенной недвижимости. "
                       "Приобретаемая недвижимость является залогом.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 80,
        },
        "min_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 50,
        },
        "max_duration": 10 * 12,
        "fine_percentage": 0.25,
        "issue_online": False,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
        ]
    },

    {
        "name": "Ганимед+",
        "description": "Кредит на приобретение строящейся недвижимости. "
                       "Приобретаемая недвижимость является залогом.",
        "annual_percentage_rate": 27,
        "max_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 90,
        },
        "min_amount": {
            "fixed": None,
            "annual_income_mul": None,
            "percent_of_purchase": 30,
        },
        "max_duration": 20 * 12,
        "fine_percentage": 0.2,
        "issue_online": False,
        "allowed_methods_of_ensuring": [
            CreditTemplate.ENSURING_PLEDGE
        ]
    },

]

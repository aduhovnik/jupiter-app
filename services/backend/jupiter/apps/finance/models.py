# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import finance.settings
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from finance.utils import money_field, percentage_field


class Product(models.Model):

    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = (
            ('view_product', 'Can view product'),
        )


class Transaction(models.Model):

    # TODO: store the action?
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    info = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        permissions = (
            ('view_transaction', 'Can view transaction'),
        )


class Contract(models.Model):

    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    signed_on = models.DateTimeField()

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        permissions = (
            ('view_contract', 'Can view contract'),
        )


class Account(Product):

    STATUS_ACTIVE = 0
    STATUS_CLOSED = 1
    STATUS_DISABLED = 2
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_DISABLED, 'Disabled'),
    ]

    # TODO: add terms?
    residue = money_field()
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Checking account'
        verbose_name_plural = 'Checking accounts'
        permissions = (
            ('view_account', 'Can view account'),
        )


class DepositTemplate(models.Model):

    INDEXING_YEARLY = 0
    INDEXING_DAILY = 1
    INDEXING_MONTHLY = 2
    INDEXING_QUARTERLY = 3
    INDEXING_CHOICES = [
        (INDEXING_YEARLY, 'Yearly'),
        (INDEXING_DAILY, 'Daily'),
        (INDEXING_MONTHLY, 'Monthly'),
        (INDEXING_QUARTERLY, 'Quarterly')
    ]

    CLOSING_ANYTIME = 0
    CLOSING_ANYTIME_WITH_LOSS = 1
    CLOSING_IN_END = 2
    CLOSING_CHOICES = [
        (CLOSING_ANYTIME, 'Anytime'),
        (CLOSING_ANYTIME_WITH_LOSS, 'Anytime with loss'),
        (CLOSING_IN_END, 'Only after end of term'),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    percentage = JSONField()
    indexing = models.IntegerField(choices=INDEXING_CHOICES, default=INDEXING_YEARLY)
    closing = models.IntegerField(choices=CLOSING_CHOICES, default=CLOSING_ANYTIME_WITH_LOSS)
    min_amount = money_field()
    max_amount = money_field(null=True)
    prolongation = models.BooleanField(default=False)
    additional_contributions = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Deposit templates'
        verbose_name_plural = 'Deposit templates'
        permissions = (
            ('view_deposittemplate', 'Can view deposit template'),
        )


class Deposit(Product):

    STATUS_ACTIVE = 0
    STATUS_CLOSED = 1
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
    ]

    amount = money_field()
    template = models.ForeignKey(DepositTemplate)
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        permissions = (
            ('view_deposit', 'Can view deposit'),
        )


class CreditTemplate(models.Model):

    ENSURING_FINE = 0
    ENSURING_PLEDGE = 1
    ENSURING_SURETY = 2
    ENSURING_CHOICES = [
        (ENSURING_FINE, "Fine"),
        (ENSURING_PLEDGE, "Plegde"),
        (ENSURING_SURETY, "Surety"),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    annual_percentage_rate = percentage_field()
    max_amount = JSONField()
    min_amount = JSONField()
    max_duration = models.IntegerField(default=12)
    fine_percentage = percentage_field()
    issue_online = models.BooleanField(default=False)
    allowed_ensuring = ArrayField(models.IntegerField(choices=ENSURING_CHOICES))

    class Meta:
        verbose_name = 'Credit templates'
        verbose_name_plural = 'Credit templates'
        permissions = (
            ('view_credittemplate', 'Can view credit template'),
        )


class Credit(Product):

    STATUS_OPENED = 0
    STATUS_FINED = 1
    STATUS_PAID_OFF = 2
    STATUS_CLOSED = 3
    STATUS_CHOICES = [
        (STATUS_OPENED, 'Opened'),
        (STATUS_FINED, 'Fined'),
        (STATUS_PAID_OFF, 'Paid off'),
        (STATUS_CLOSED, 'Closed'),
    ]

    residue = money_field()
    current_penalty = money_field()
    next_payment_term = models.DateField()
    template = models.ForeignKey(CreditTemplate)
    status = models.IntegerField(choices=STATUS_CHOICES)
    fine_percentage = percentage_field()
    method_of_ensuring = models.IntegerField(choices=CreditTemplate.ENSURING_CHOICES)

    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        permissions = (
            ('view_credit', 'Can view credit'),
        )

from django.db import models
from django.conf import settings

from utils import money_field, percentage_field


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
    ACTIVE = 0
    CLOSED = 1
    DISABLED = 2
    STATUSES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
        (DISABLED, 'Disabled'),
    ]

    # TODO: add terms?
    residue = money_field()
    status = models.IntegerField(choices=STATUSES, )

    class Meta:
        verbose_name = 'Checking account'
        verbose_name_plural = 'Checking accounts'
        permissions = (
            ('view_account', 'Can view account'),
        )


class DepositTemplate(models.Model):

    YEARLY = 0
    DAILY = 1
    MONTHLY = 2
    QUARTERLY = 3
    INDEXATIONS = [
        (YEARLY, 'Yearly'),
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly')
    ]

    ANYTIME = 0
    ANYTIME_WITH_LOSSY = 1
    ONLY_AFTER_END = 2

    CONCELLATION_CONDITIONS = [
        (ANYTIME, 'Anytime'),
        (ANYTIME_WITH_LOSSY, 'Anytime with lossy'),
        (ONLY_AFTER_END, 'Only after end of term'),
    ]

    name = models.CharField(max_length=100)
    percentage = percentage_field()
    indexing = models.IntegerField(choices=INDEXATIONS)
    cancellation_condition = models.IntegerField(choices=CONCELLATION_CONDITIONS)
    duration = models.DurationField()
    min_amount = money_field()
    max_amount = money_field()
    prolongation = models.BooleanField()

    class Meta:
        verbose_name = 'Deposit templates'
        verbose_name_plural = 'Deposit templates'
        permissions = (
            ('view_deposittemplate', 'Can view deposit template'),
        )

class Deposit(Product):
    ACTIVE = 0
    CLOSED = 1
    STATUSES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    ]

    amount = money_field()
    template = models.ForeignKey(DepositTemplate)
    status = models.IntegerField(choices=STATUSES)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        permissions = (
            ('view_deposit', 'Can view deposit'),
        )

class CreditTemplate(models.Model):
    name = models.CharField(max_length=100)
    percentage = percentage_field()
    duration = models.DurationField()
    min_amount = money_field()
    max_amount = money_field()
    monthly_payment = money_field()
    fine_percentage = percentage_field()
    issue_online = models.BooleanField()

    # TODO: Indexing?
    # TODO: line of credit or a one-time issue?

    class Meta:
        verbose_name = 'Credit templates'
        verbose_name_plural = 'Credit templates'
        permissions = (
            ('view_credittemplate', 'Can view credit template'),
        )

class Credit(Product):
    OPENED = 0
    FINED = 1
    PAID_OFF = 2
    CLOSED = 3
    STATUSES = [
        (OPENED, 'Opened'),
        (FINED, 'Fined'),
        (PAID_OFF, 'Paid off'),
        (CLOSED, 'Closed'),
    ]

    residue = money_field()
    template = models.ForeignKey(CreditTemplate)
    status = models.IntegerField(choices=STATUSES)
    # TODO: fine in percent?
    fine_percentage = percentage_field()

    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        permissions = (
            ('view_credit', 'Can view credit'),
        )
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import random
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

from finance.utils import money_field, percentage_field
from finance.bank_system_proxy import BankSystemProxy


class Product(models.Model):

    is_active = models.BooleanField(default=False)
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
    signed_on = models.DateTimeField(auto_now_add=True)

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
    STATUS_REJECTED = 3
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_DISABLED, 'Disabled'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    INOPERABLE_STATUSES = [
        STATUS_DISABLED,
        STATUS_REJECTED,
        STATUS_CLOSED
    ]

    number = models.CharField(max_length=13, default='0' * 13)
    residue = money_field()
    status = models.IntegerField(choices=STATUS_CHOICES)
    close_claim = models.BooleanField(default=False)
    target_account_id = models.IntegerField(default=-1)

    class Meta:
        verbose_name = 'Checking account'
        verbose_name_plural = 'Checking accounts'
        permissions = (
            ('view_account', 'Can view account'),
        )

    @classmethod
    def _create_new_number(cls):
        new_number = '301400' + str(random.randrange(1000000, 9999999))
        while cls.objects.filter(number=new_number):
            new_number = '301400' + str(random.randrange(1000000, 9999999))
        return new_number

    @classmethod
    def create(cls, is_active, client, first_contribution):
        """
        account created already with money - dummy
        Also, if credit opened, then money can be puted into created account
        """
        account = Account.objects.create(
            is_active=is_active,
            number=cls._create_new_number(),
            residue=first_contribution,
            status=Account.STATUS_ACTIVE,
            client=client
        )
        account.save()
        info_text = 'Создан счет' if is_active else 'Подана заявка на создание счета'
        Transaction.objects.create(client=client,
                                   product=account,
                                   info=info_text)
        return account

    @classmethod
    def assign(cls, client, account_number):
        """
        assign account by account_number to client
        """
        if Account.objects.filter(number=account_number):
            return False, 'Этот счет уже используется.'
        res, money_amount = BankSystemProxy.account_assign_to_user(client, account_number)
        if not res:
            return False, 'Отказано банком. Проверте счет.'
        account = Account.objects.create(
            number=account_number,
            is_active=True,
            residue=money_amount,
            status=Account.STATUS_ACTIVE,
            client=client
        )
        account.save()
        info_text = 'Счет успешно привязан.'
        Transaction.objects.create(client=client,
                                   product=account,
                                   info=info_text)
        return True, info_text

    def confirm(self):
        """
        Confirm account
        """
        if self.is_active:
            return False

        bank_confirmation = BankSystemProxy.account_creation(self.number,
                                                             self.client.id,
                                                             float(self.residue.amount))
        if not bank_confirmation:
            self.reject('Отклонено банком')
            return False

        self.is_active = True
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Счет подтвержден.')
        Contract.objects.create(client=self.client,
                                product=self)
        return True

    def reject(self, cause):
        if self.is_active:
            return False
        self.status = Account.STATUS_REJECTED
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на создание счета отклонена. Причина: {}'.format(cause))
        return True

    def put_money(self, contribution):
        """
        In BYN only
        """
        if not self.is_active or self.status in Account.INOPERABLE_STATUSES:
            return False

        bank_confirmation = BankSystemProxy.account_put_money(self.id, float(contribution))
        if not bank_confirmation:
            return False

        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Зачисление в размере {} BYN'.format(contribution))
        self.residue.amount += Decimal(contribution)
        self.save()
        return True

    def get_money(self, required_quantity):
        """
        In BYN only
        """
        if not self.is_active or self.status in Account.INOPERABLE_STATUSES:
            return False
        if self.residue.amount >= required_quantity:
            self.residue.amount -= Decimal(required_quantity)
            self.save()

            bank_confirmation = BankSystemProxy.account_get_money(self.id,
                                                                  required_quantity)
            if not bank_confirmation:
                return False

            Transaction.objects.create(client=self.client,
                                       product=self,
                                       info='Снятие в размере {} BYN'.format(required_quantity))
            return True
        return False

    def leave_close_claim(self, target_account_id=None):
        """
        :param target_account_id:
        account_id, where money will be sent
        """
        if not self.is_active or self.status in Account.INOPERABLE_STATUSES:
            return False
        if not (target_account_id is None):
            self.target_account_id = target_account_id
        self.close_claim = True
        self.save()
        return True

    def close_confirm(self):
        if not self.is_active or self.status in Account.INOPERABLE_STATUSES:
            return False
        if not self.close_claim:
            return False
        if self.residue.amount > 0.1 and self.target_account_id != -1:
            target_account = Account.objects.get(pk=self.target_account_id)
            target_account.put_money(self.residue.amount)

        bank_confirmation = BankSystemProxy.account_closing(self.id)
        if not bank_confirmation:
            self.close_reject('Отклонено банком.')
            return False

        self.status = Account.STATUS_CLOSED
        self.close_claim = False
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Счет закрыт, деньги переведены на счет {}.'.format(self.target_account_id))
        return True

    def close_reject(self, cause):
        if not self.is_active or self.status in Account.INOPERABLE_STATUSES:
            return False
        if not self.close_claim:
            return False
        self.close_claim = False
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Закрытие счета отклонено. Причина: {}.'.format(cause))
        return True


class DepositTemplate(models.Model):

    CAPITALIZATION_YEARLY = 0
    CAPITALIZATION_DAILY = 1
    CAPITALIZATION_MONTHLY = 2
    CAPITALIZATION_QUARTERLY = 3
    CAPITALIZATION_CHOICES = [
        (CAPITALIZATION_YEARLY, 'Yearly'),
        (CAPITALIZATION_DAILY, 'Daily'),
        (CAPITALIZATION_MONTHLY, 'Monthly'),
        (CAPITALIZATION_QUARTERLY, 'Quarterly')
    ]

    CLOSING_ANYTIME = 0
    CLOSING_IN_END = 1
    CLOSING_CHOICES = [
        (CLOSING_ANYTIME, 'Anytime'),
        (CLOSING_IN_END, 'Only after end of term'),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    currency = JSONField()
    capitalization = models.IntegerField(choices=CAPITALIZATION_CHOICES, default=CAPITALIZATION_MONTHLY)
    closing = models.IntegerField(choices=CLOSING_CHOICES, default=CLOSING_IN_END)
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
    STATUS_REJECTED = 2
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    CAPITALIZATION_TIME_PERIOD = [
        relativedelta(years=1),
        relativedelta(days=1),
        relativedelta(months=1),
        relativedelta(months=3),
    ]

    CAPITALIZATION_COEFFICIENT = [
        Decimal(1.0),
        Decimal(1.0 / 365.0),
        Decimal(1.0 / 12.0),
        Decimal(3.0 / 12.0),
    ]

    amount = money_field()
    template = models.ForeignKey(DepositTemplate)
    status = models.IntegerField(choices=STATUS_CHOICES)
    start_date = models.DateField()
    percentage = percentage_field()
    capitalization = models.IntegerField(choices=DepositTemplate.CAPITALIZATION_CHOICES)
    closing = models.IntegerField(choices=DepositTemplate.CLOSING_CHOICES)
    duration = models.IntegerField(default=12)
    prolongation = models.BooleanField(default=False)
    additional_contributions = models.BooleanField(default=False)
    next_capitalize_term = models.DateField(null=True)
    currency = models.CharField(default='BYN', max_length=20)  # DUMMY
    source_account_id = models.IntegerField(default=-1)  # money source
    target_account_id = models.IntegerField(default=-1)  # money destination
    close_claim = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        permissions = (
            ('view_deposit', 'Can view deposit'),
        )

    @classmethod
    def create(cls, client, template, money_amount, duration, percentage, currency, account_id):
        """
        Deposit claim, them admin should allow it
        Currencies: BYN, USD, EUR
        """
        need_byn = BankSystemProxy.get_currency_rate()[currency] * money_amount
        account = Account.objects.get(pk=account_id)
        if account.residue.amount >= need_byn:
            deposit = cls.objects.create(
                is_active=False,
                client=client,
                template=template,
                amount=money_amount,
                start_date=datetime.date.today() + relativedelta(days=1),
                status=cls.STATUS_ACTIVE,
                percentage=percentage,
                currency=currency,
                capitalization=template.capitalization,
                closing=template.closing,
                prolongation=template.prolongation,
                additional_contributions=template.additional_contributions,
                next_capitalize_term=datetime.date.today() + cls.CAPITALIZATION_TIME_PERIOD[template.capitalization],
                duration=duration,
                source_account_id=account_id
            )
            deposit.save()
            account.status = Account.STATUS_DISABLED
            account.save()
            Transaction.objects.create(client=client,
                                       product=deposit,
                                       info='Подана заявка на депозит.')
            return deposit
        return None

    def confirm(self):
        """
        Confirm deposit, defreeze account and transfer money
        """
        if self.status in Credit.INOPERABLE_STATUSES or self.is_active:
            return False

        bank_confirmation = BankSystemProxy.deposit_creation(self.client.id,
                                                             self.template.id,
                                                             self.duration,
                                                             float(self.percentage),
                                                             float(self.amount.amount),
                                                             self.currency)
        if not bank_confirmation:
            self.reject('Отказано банком.')
            return False

        self.is_active = True
        account = Account.objects.get(pk=self.source_account_id)
        money_in_byn = BankSystemProxy.get_currency_rate()[self.currency] * float(self.amount.amount)
        account.status = Account.STATUS_ACTIVE
        account.get_money(money_in_byn)
        account.save()
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Депозит открыт.')
        Contract.objects.create(client=self.client,
                                product=self)
        return True

    def reject(self, cause):
        if self.status in Credit.INOPERABLE_STATUSES:
            return False
        self.status = Deposit.STATUS_REJECTED
        account = Account.objects.get(pk=self.source_account_id)
        account.status = Account.STATUS_ACTIVE
        account.save()
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на депозит отклонена. Причина: {}'.format(cause))
        return True

    def leave_close_claim(self, target_account_id):
        """
        Close deposit and transfer money to account
        If deposit.closing = CLOSING_ANYTIME  - just transfer current amount to account_id
        if deposit.closing = CLOSING_IN_END then
        deposit can be closed in period +-1 week about and date
        """
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False, 'Операции с кредитом невозможны.'
        if self.closing == DepositTemplate.CLOSING_IN_END:
            cur_date = datetime.date.today()
            end_date = self.start_date + relativedelta(months=self.duration)
            if end_date + relativedelta(days=-7) < cur_date < end_date + relativedelta(days=7):
                self.close_claim = True
                self.target_account_id = target_account_id
                self.save()
                return True, 'Ваша заявка будет рассмотрена'
            return False, 'Вы можете забрать депозит только начиная с {}'.\
                format(str(end_date + relativedelta(days=-7)))
        else:
            self.close_claim = True
            self.target_account_id = target_account_id
            self.save()
            return True, 'Вы можете забрать депозит в данный момент. Ваша заявка будет рассмотрена'

    def close_confirm(self):
        if not self.close_claim:
            return False
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False

        bank_confirmation = BankSystemProxy.deposit_closing(self.id)
        if not bank_confirmation:
            self.reject('Отказано банком.')
            return False

        cur_date = datetime.date.today()
        end_date = self.start_date + relativedelta(months=self.duration)
        if self.next_capitalize_term < min(end_date, cur_date):  # last capitalize, if need
            self._update_amount()
        money_in_byn = BankSystemProxy.get_currency_rate()[self.currency] * float(self.amount.amount)
        account = Account.objects.get(pk=self.target_account_id)
        account.put_money(money_in_byn)
        self.status = self.STATUS_CLOSED
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Депозит закрыт. Деньги в размере {} BYN переведены на счет {}'.
                                   format(money_in_byn, self.target_account_id))
        return True

    def close_reject(self, cause):
        if not self.close_claim:
            return False
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False
        self.close_claim = False
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Отказано в закрытие депозита. Причина: {}.'.format(cause))
        return True

    def additional_contribution(self, money_amount):
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False
        if not self.additional_contributions:
            return False
        money_in_cur = float(money_amount) / BankSystemProxy.get_currency_rate()[self.currency]
        self.amount.amount += Decimal(money_in_cur)
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Начислены деньги на депозит.')
        return True

    def daily_update(self):
        """
        Recalculate(capitalize) money amount and set new capitalize term
        If deposit duration has ended --> close or prolongate deposit
        Give 1 week buffer for client before longation
        """
        cur_date = datetime.date.today()
        if self.start_date + relativedelta(months=self.duration) + relativedelta(days=7) < cur_date:
            if self.prolongation:
                self.start_date += relativedelta(months=self.duration)
                self.next_capitalize_term += Deposit.CAPITALIZATION_TIME_PERIOD[self.capitalization]
                Transaction.objects.create(client=self.client,
                                           product=self,
                                           info='Совершено пролонгирование депозита.')
            else:
                self.status = Deposit.STATUS_CLOSED
        elif self.next_capitalize_term <= cur_date:
            self._update_amount()
            Transaction.objects.create(client=self.client,
                                       product=self,
                                       info='Начисление процентов. Новая сумма депозита: {}.'.format(self.amount))
        self.save()

    def _update_amount(self):
        self.next_capitalize_term += Deposit.CAPITALIZATION_TIME_PERIOD[self.capitalization]
        coef = Deposit.CAPITALIZATION_COEFFICIENT[self.capitalization]
        self.amount.amount += self.amount.amount * (self.percentage / Decimal(100.0)) * coef
        self.save()


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
    STATUS_REJECTED = 4
    STATUS_CHOICES = [
        (STATUS_OPENED, 'Opened'),
        (STATUS_FINED, 'Fined'),
        (STATUS_PAID_OFF, 'Paid off'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    INOPERABLE_STATUSES = [
        STATUS_CLOSED,
        STATUS_REJECTED
    ]

    INTO_ACCOUNT = 0  # Your account or seller account
    IN_CASH = 1

    MONEY_DESTINATION = [
        (INTO_ACCOUNT, 'Into account'),
        (IN_CASH, 'In cash'),
    ]

    total_sum = money_field()
    residue = money_field()
    current_penalty = money_field()
    start_date = models.DateField()
    duration = models.IntegerField()  # in months
    next_payment_term = models.DateField(null=True)
    template = models.ForeignKey(CreditTemplate)
    status = models.IntegerField(choices=STATUS_CHOICES)
    annual_percentage_rate = percentage_field()
    fine_percentage = percentage_field()
    minimum_monthly_pay = money_field(null=True)
    current_month_pay = money_field(null=True)
    current_month_percents = money_field(null=True)  # money amount, should be payed, to avoid penalty
    method_of_ensuring = models.IntegerField(choices=CreditTemplate.ENSURING_CHOICES)
    money_destination = models.IntegerField(choices=MONEY_DESTINATION)
    target_account_id = models.IntegerField(default=-1)  # where money will be placed

    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        permissions = (
            ('view_credit', 'Can view credit'),
        )

    def close(self):
        """
        User can close credit without confirmation, if credit is paid_off
        Attempts to close the credit. Throws exceptions if the attempt fails
        """
        if self.status != Credit.STATUS_PAID_OFF:
            return False

        bank_confirmation = BankSystemProxy.credit_close(self.id)
        if not bank_confirmation:
            return False

        self.status = Credit.STATUS_CLOSED
        self.save()
        return True

    def current_percents(self):
        return Credit._get_current_percentage(self.residue.amount, self.annual_percentage_rate)

    def daily_update(self):
        """
        Updates the state of the model. Should be called daily
        """
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return
        self._check_overdue()
        if self.status == Credit.STATUS_FINED:
            self._update_penalty()
            Transaction.objects.create(client=self.client,
                                       product=self,
                                       info='Начислен штраф. Текущий штраф: {}.'.format(self.current_penalty))
        self.save()

    def pay(self, payment):
        """
        Processes the payment for the credit.
        Steps:
            0. assert credit != CLOSED
            1. If credit FINED, then
                a. Try to pay penalty
                b. If penalty payed, then change credit status to OPENED, then continue
            2. If credit OPENED or PAYED_OFF(client should explicitly close credit), then
                Every payment goes to pay for current credit percents and for decrease residue, so
                a. Pay for percents
                b. Decrease residue
                c. Inc current_month_pay
        We can multiple payments during one month.
        """
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False

        bank_confirmation = BankSystemProxy.credit_pay(self.id, payment)
        if not bank_confirmation:
            return False

        payment = Decimal(payment)
        self.total_sum.amount += payment
        if self.status == Credit.STATUS_FINED:
            if self.current_penalty.amount <= payment:
                payment, self.current_penalty.amount = payment - self.current_penalty.amount, 0
                self.status = Credit.STATUS_OPENED
            else:
                self.current_penalty.amount -= payment
                payment = 0
        self.current_month_pay.amount += payment  # inc current_month_pay
        cur_percents = self.current_month_percents.amount
        cur_percents, payment = max(0, cur_percents - payment), max(0, payment - cur_percents)
        self.current_month_percents = cur_percents
        self.residue.amount -= payment  # can be < 0
        if self.residue.amount <= 0:
            self.status = Credit.STATUS_PAID_OFF
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Внесен платеж по кредиту в размере: {}.'.format(payment))
        self.save()
        return True

    def _check_overdue(self):
        """
        Checks for overdue and updates accordingly. Should be called daily
        """
        # If new month began - set next payment term, and current_month_percents will be computed
        # If credit is overdue - set status FINED, then penalty will be calculated
        # If the entire term of the loan left - then FINED anyway
        # PS: credit.next_payment_term - is NOT last day, client should pay before this date
        cur_date = datetime.date.today()
        end_date = self.start_date + relativedelta(month=self.duration)
        if end_date <= cur_date:
            self.status = Credit.STATUS_FINED
        elif self.next_payment_term <= cur_date:
            if self.current_month_percents != 0:
                self.status = Credit.STATUS_FINED
            else:
                self.next_payment_term += relativedelta(months=1)
                #  +0.1 - symbolic accrual, need if credit PAYED but NOT CLOSED
                self.current_month_percents = self.current_percents() + 0.1
                self.current_month_pay.amount = 0
        self.save()

    def _update_penalty(self):
        """
        Recalculates the penalty. Should be called daily
        """
        # inc by fine_percent from pure RESIDUE+PENALTY, till penalty will be payed
        # fine_percent got taken from credit template
        if self.status == Credit.STATUS_FINED:
            total = self.residue.amount + self.current_penalty.amount
            self.current_penalty = self.current_penalty.amount + total * self.fine_percentage / Decimal(100.0)
        self.save()

    @classmethod
    def _credit_scoring(cls):
        return True

    @classmethod
    def create_online(cls, client, template, money_amount,
                      duration, account_id=None):

        bank_confirmation = BankSystemProxy.credit_create(client.id,
                                                          template.id,
                                                          money_amount,
                                                          duration,
                                                          float(template.annual_percentage_rate))
        if not bank_confirmation:
            return False, 'Отказано банком'

        # PLACEHOLDER FOR CREDIT SCORING
        if not cls._credit_scoring():
            return False, 'Ваша заявка отклонена кредитным скорингом'

        monthly_pay = cls._min_monthly_pay(money_amount, template.annual_percentage_rate, duration)
        # Create account if need
        if account_id is None:
            account = Account.create(True, client, 0)
            account_id = account.id
        credit = cls.objects.create(
            is_active=True,
            client=client,
            template=template,
            total_sum=0,
            residue=money_amount,
            current_penalty=0,
            start_date=datetime.date.today() + relativedelta(months=1),
            duration=duration,
            next_payment_term=datetime.date.today() + relativedelta(months=2),
            status=cls.STATUS_OPENED,
            annual_percentage_rate=template.annual_percentage_rate,
            fine_percentage=template.fine_percentage,
            minimum_monthly_pay=monthly_pay,
            current_month_pay=0,
            current_month_percents=0,
            method_of_ensuring=CreditTemplate.ENSURING_FINE,
            money_destination=cls.INTO_ACCOUNT,
            target_account_id=account_id
        )
        credit.save()
        target_account = Account.objects.get(pk=account_id)
        target_account.put_money(money_amount)
        target_account.save()

        info_text = 'Открыт онлайн кредит кредит.'
        Transaction.objects.create(client=client,
                                   product=credit,
                                   info=info_text)
        return True, credit

    @classmethod
    def create_claim(cls, client, template, money_amount, duration, ensuring_method,
                     money_destination=INTO_ACCOUNT, account_id=None):
        """
        if Template.issue_online, then credit will be created as active
        Creates a credit with default parameters.
        Client gets 1 month, as buffered - no payment, then begin loan payments.
        """
        monthly_pay = cls._min_monthly_pay(money_amount, template.annual_percentage_rate, duration)
        # create account, if need
        if account_id is None and money_destination == cls.INTO_ACCOUNT:
            account = Account.create(False, client, 0)
            account_id = account.id
        if account_id is None:
            account_id = -1
        credit = cls.objects.create(
            is_active=False,
            client=client,
            template=template,
            total_sum=0,
            residue=money_amount,
            current_penalty=0,
            start_date=datetime.date.today() + relativedelta(months=1),
            duration=duration,
            next_payment_term=datetime.date.today() + relativedelta(months=2),
            status=cls.STATUS_OPENED,
            annual_percentage_rate=template.annual_percentage_rate,
            fine_percentage=template.fine_percentage,
            minimum_monthly_pay=monthly_pay,
            current_month_pay=0,
            current_month_percents=0,
            method_of_ensuring=ensuring_method,
            money_destination=money_destination,
            target_account_id=account_id
        )

        info_text = 'Подана заявка на кредит.'
        Transaction.objects.create(client=client,
                                   product=credit,
                                   info=info_text)
        return credit

    def confirm(self):
        if self.is_active:
            return False
        if self.status in Credit.INOPERABLE_STATUSES:
            return False
        bank_confirmation = BankSystemProxy.credit_create(self.client.id,
                                                          self.template.id,
                                                          float(self.residue.amount),
                                                          self.duration,
                                                          float(self.annual_percentage_rate))
        if not bank_confirmation:
            self.reject('Отказано банком')
            return False

        if self.money_destination == Credit.INTO_ACCOUNT:
            account = Account.objects.get(pk=self.target_account_id)
            account.confirm()
            account.put_money(self.residue.amount)
            account.save()

        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на кредит одобрена.')

        Contract.objects.create(client=self.client,
                                product=self)
        self.is_active = True
        self.save()
        return True

    def reject(self, cause):
        if self.status in Credit.INOPERABLE_STATUSES or not self.is_active:
            return False
        self.status = Credit.STATUS_REJECTED
        self.save()
        account = Account.objects.get(pk=self.target_account_id)
        if not account.is_active:
            account.reject(cause)
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на кредит отклонена. Причина: {}'.format(cause))
        return True

    @staticmethod
    def _get_current_percentage(residue, percentage):
        """
        Percents for current residue from last month
        """
        # TODO: 30 days in a month and 365 in a year? #Yes!
        r = Decimal(residue)
        p = Decimal(percentage)
        return r * (p / Decimal(100.0)) * Decimal(30) / Decimal(365)

    @staticmethod
    def _min_monthly_pay(payment, percentage, duration):
        """
        This work in that way - func return value, allow you to payed credit till credit term,
        if you are not fall into the penalty
        The less each payment - the greater the overpayment.
        (yes, it can be sum of geom progression)
        """
        coef = Decimal(1.0) + percentage / Decimal(100.0) / Decimal(12.0)
        mult = Decimal(1.0) / coef
        for _ in range(duration):
            mult = (mult + Decimal(1.0)) / coef
        return payment / mult

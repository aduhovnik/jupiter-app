from .models import Credit, Deposit

# TODO: schedule to execute every day
# TODO: mb use https://github.com/tivix/django-cron


def daily_tasks():
    update_credits()
    update_deposits()


def update_credits():
    objects = Credit.objects.exclude(status__in=[Credit.STATUS_CLOSED, Credit.STATUS_REJECTED])\
                            .exclude(is_active__in=[False])
    for credit in objects:
        credit.daily_update()


def update_deposits():
    objects = Deposit.objects.exclude(status__in=[Deposit.STATUS_CLOSED, Deposit.STATUS_REJECTED])\
                             .exclude(is_active__in=[False])
    for deposit in objects:
        deposit.daily_update()

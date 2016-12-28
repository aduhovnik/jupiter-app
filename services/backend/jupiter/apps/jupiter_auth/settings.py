# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


CLIENTS_GROUP = 'Clients'
ADMINS_GROUP = 'Admins'
GROUPS = [
    {
        "name": CLIENTS_GROUP,
        "permissions": [
            'manage_himself',
            'view_credit',
            'add_credit',
            'change_credit',
            'add_account',
            'change_credit',
            'view_account',
            'add_account',
            'change_account',
            'view_deposit',
            'add_deposit',
            'change_deposit',
            'view_contract',
            'view_transaction',
        ]
    },
    {
        "name": ADMINS_GROUP,
        "permissions": [
            'manage_himself',
            'view_user',
            'view_credit',
            'add_credit',
            'change_credit',
            'add_account',
            'change_credit',
            'view_account',
            'add_account',
            'change_account',
            'view_deposit',
            'add_deposit',
            'change_deposit',
            'view_contract',
            'view_transaction',
            'change_user',
        ]
    }
]



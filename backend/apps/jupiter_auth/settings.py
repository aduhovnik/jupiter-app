# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


CLIENTS_GROUP = 'Clients'
ADMINS_GROUP = 'Admins'
GROUPS = [
    {
        "name": CLIENTS_GROUP,
        "permissions": [
            'manage_himself',
        ]
    },
    {
        "name": ADMINS_GROUP,
        "permissions": []
    }
]

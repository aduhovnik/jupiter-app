# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from django.conf.urls import url, include


def collect_applications():
    backend_path = os.environ.get('BACKEND_PATH', '..')
    apps_path = os.path.join(backend_path, 'apps')
    apps = []
    for filename in os.listdir(apps_path):
        if os.path.isdir(os.path.join(apps_path, filename)):
            apps.append('apps.{}'.format(filename))
    return apps


def collect_urls():
    return [
        url(r'^', include(app))
        for app in collect_applications()
    ]

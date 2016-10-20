# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.viewsets import ModelViewSet as BaseModelViewSet
from rest_framework.viewsets import GenericViewSet as BaseGenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet as BaseReadOnlyModelViewSet
from core.api.generic.mixins import FieldsViewMixin, OrderingViewMixin, FilteringViewMixin


class GenericViewSet(FieldsViewMixin,
                     OrderingViewMixin,
                     FilteringViewMixin,
                     BaseGenericViewSet):
    pass


class ModelViewSet(BaseModelViewSet, GenericViewSet):
    pass


class ReadOnlyModelViewSet(BaseReadOnlyModelViewSet, GenericViewSet):
    pass

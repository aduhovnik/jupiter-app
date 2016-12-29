# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from finance.models import FinanceSettings


class FinanceSettingsSerializer(serializers.ModelSerializer):

    scoring = serializers.DictField(required=True)
    currencies = serializers.ListField(read_only=True)
    exchange_rates = serializers.DictField(read_only=True)

    def validate(self, attrs):
        attrs = super(FinanceSettingsSerializer, self).validate(attrs)
        scoring_settings = attrs['scoring']
        if not 'warning_level' in scoring_settings:
            raise ValidationError('warning_level is required field')
        if not 'danger_level' in scoring_settings:
            raise ValidationError('danger_level is required field')

        try:
            scoring_settings['warning_level'] = float(scoring_settings['warning_level'])
            scoring_settings['danger_level'] = float(scoring_settings['danger_level'])
        except Exception:
            raise ValidationError('Число в неверном формате')

        if scoring_settings['warning_level'] <= scoring_settings['danger_level']:
            raise ValidationError('danger_level must be less than warning_level')
        if not 0 <= scoring_settings['warning_level'] <= 1:
            raise ValidationError('warning_level mush be in range of [0, 1]')
        if not 0 <= scoring_settings['danger_level'] <= 1:
            raise ValidationError('danger_level mush be in range of [0, 1]')
        return attrs

    class Meta:
        model = FinanceSettings
        fields = (
            'scoring',
            'currencies',
            'exchange_rates'
        )
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from jupiter_auth.models import UserProfile
from rest_framework.serializers import ModelSerializer, ValidationError


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = (
            'id',
            'user'
        )

    def validate(self, value):
        """
        общий вид идентификационного номера:
        ЦЦЦЦЦЦЦ Б ЦЦЦ ББ Ц
        ^\d{7}[A-Z]{1}\d{3}[A-Z]{2}\d{1}$
        общий вид номера паспорта паспорта:
        2 буквы ЦЦЦЦЦЦЦ
        AB	Брестская область
        BM	Витебская область
        HB	Гомельская область
        KH	Гродненская область
        MP	город Минск
        MC	Минская область
        KB	Могилевская область
        PP  Для иностранного проживания
        """
        super(UserProfileSerializer, self).validate(value)
        errors = {}
        passport_number = value['passport_number']
        identification_number = value['identification_number']
        if re.match('^(AB|BM|HB|KH|MP|MC|KB|PP)\d{7}$', passport_number) is None:
            errors['passport_number'] = 'Номер паспорта должен иметь формат (AB|BM|HB|KH|MP|MC|KB|PP) ЦЦЦЦЦЦЦ.'
        if re.match('^\d{7}[A-Z]{1}\d{3}[A-Z]{2}\d{1}$', identification_number) is None:
            errors['identification_number'] = 'Идентификационный номер должен подходить под формат ЦЦЦЦЦЦЦ Б ЦЦЦ ББ Ц.'
        if len(errors):
            raise ValidationError(errors)
        return value


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'name',
        )


class UserSerializer(ModelSerializer):

    profile = UserProfileSerializer()
    groups = GroupSerializer(many=True, read_only=True)

    def update(self, obj, validated_data):
        profile_data = validated_data.pop('profile')
        serializer = UserProfileSerializer(instance=obj.profile, data=profile_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super(UserSerializer, self).update(obj, validated_data)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
            'groups',
            'is_active',
        )

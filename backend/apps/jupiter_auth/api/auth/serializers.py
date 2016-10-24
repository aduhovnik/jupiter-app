# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from jupiter_auth.settings import CLIENTS_GROUP


class SignInSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class SignUpSerializer(serializers.ModelSerializer):

    is_active = serializers.CreateOnlyDefault(True)

    def create(self, validated_data):
        instance = get_user_model().objects.create_user(**validated_data)
        instance.groups.add(Group.objects.get(name=CLIENTS_GROUP))
        return instance

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )

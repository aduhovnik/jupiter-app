# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from jupiter_auth.models import UserProfile
from rest_framework.serializers import ModelSerializer


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = (
            'user', 'id'
        )


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'name',
        )


class UserSerializer(ModelSerializer):

    profile = UserProfileSerializer()
    groups = GroupSerializer(many=True)

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
        )

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from jupiter_auth.models import UserProfile
from rest_framework.serializers import ModelSerializer


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = (
            'id',
            'user'
        )


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

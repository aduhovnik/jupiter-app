# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from core.utils import send_mail
from core.api.generic.views import ModelViewSet
from jupiter_auth.utils import get_or_create_clients_group, get_or_create_admins_group
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.api.users.serializers import UserSerializer


class UserView(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (ManageSelfPermission,)

    def get_queryset(self):
        queryset = super(UserView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        elif self.kwargs.get(self.lookup_field) == 'me':
            return queryset.filter(pk=self.request.user.pk)
        elif get_or_create_admins_group() in self.request.user.groups.all():
            return queryset.filter(groups=get_or_create_clients_group())
        else:
            return queryset.none()

    def get_object(self):
        if self.kwargs[self.lookup_field] == 'me':
            return self.request.user
        else:
            return super(UserView, self).get_object()

    @detail_route(methods=['GET'])
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            raise ValidationError('Пользователь уже активирован')

        user.is_active = True
        user.save()

        message = render_to_string('auth/account_confirm_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт подтвержден', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            raise ValidationError('Пользователь уже деактивирован')

        user.is_active = False
        user.save()

        message = render_to_string('auth/account_deactivate_email.html')
        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт отключен', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

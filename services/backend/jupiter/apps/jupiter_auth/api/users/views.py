# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.template import Context
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from core.utils import send_mail
from core.api.generic.views import ReadOnlyModelViewSet
from jupiter_auth.api.users.permissions import ManageSelfPermission
from jupiter_auth.authentication import TokenAuthentication
from jupiter_auth.api.users.serializers import UserSerializer


class UserView(ReadOnlyModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (ManageSelfPermission,)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'me':
            self.kwargs[self.lookup_field] = getattr(self.request.user, self.lookup_field)
        return super(UserView, self).retrieve(request, *args, **kwargs)

    @detail_route(methods=['GET'])
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            raise ValidationError('Пользователь уже активирован')

        context = {"link": "https://jupiter-group.tk/admin/"}
        message = render_to_string('auth/accound_confirm_email.html', context=context)

        try:
            send_mail('no-reply@jupiter-group.com', user.email, 'Ваш аккаунт подтвержден', message)
        except Exception as e:
            raise ValidationError('Ошибка при отправке письма: {}'.format(e))
        return Response(status=status.HTTP_200_OK)

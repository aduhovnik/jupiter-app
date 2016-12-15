# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from jupiter_auth.authentication import sign_in, sign_out, TokenAuthentication
from jupiter_auth.api.auth.serializers import SignInSerializer, SignUpSerializer


class SignInView(CreateModelMixin, GenericViewSet):

    authentication_classes = ()
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = sign_in(**serializer.validated_data)
        return Response({"token": token.key}, status.HTTP_200_OK)


class SignOutView(ListModelMixin, GenericViewSet):

    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        sign_out(request.query_params.get('token'))
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpView(CreateModelMixin, GenericViewSet):

    authentication_classes = ()
    serializer_class = SignUpSerializer

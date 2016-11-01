# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import factory
from django.contrib.auth.models import User
from faker import Faker
from jupiter_auth.models import UserProfile


fake = Faker()


class UserProfileFactory(factory.DjangoModelFactory):

    identification_number = factory.sequence(lambda n: fake.ssn())
    passport_number = factory.sequence(lambda n: fake.ssn())
    phone = factory.sequence(lambda n: fake.phone_number())
    address = factory.sequence(lambda n: fake.address())
    age = factory.sequence(lambda n: fake.pydecimal(left_digits=2, right_digits=0, positive=True))
    passport_expires = factory.sequence(lambda n: fake.date())
    birth_date = factory.sequence(lambda n: fake.date())
    family_status = factory.sequence(lambda n: fake.sentence(nb_words=5))
    dependants = factory.sequence(lambda n: fake.sentence(nb_words=10))
    income = factory.sequence(lambda n: fake.sentence(nb_words=4))
    realty = factory.sequence(lambda n: fake.sentence(nb_words=15))
    job = factory.sequence(lambda n: "{}, {}".format(fake.company(), fake.job()))
    user = factory.SubFactory('jupiter_auth.factories.UserFactory', profile=None)

    class Meta:
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):

    username = factory.lazy_attribute(lambda obj: "{}.{}".format(obj.first_name, obj.last_name))
    email = factory.lazy_attribute(lambda obj: "{}@gmail.com".format(obj.username))
    first_name = factory.sequence(lambda n: fake.first_name())
    last_name = factory.sequence(lambda n: fake.last_name())
    profile = factory.RelatedFactory(UserProfileFactory, 'user')
    password = 'password'

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted:
            self.groups.add(*extracted)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if extracted:
            self.user_permissions.add(*extracted)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = User.objects.filter(username=kwargs.get('username')).first()
        if user:
            return user
        else:
            is_superuser = kwargs.get('is_superuser')
            if is_superuser:
                return User.objects.create_superuser(*args, **kwargs)
            else:
                return User.objects.create_user(*args, **kwargs)

    class Meta:
        model = User

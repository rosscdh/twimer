# -*- coding: UTF-8 -*-
import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.Factory):
    FACTORY_FOR = get_user_model()

    username = 'wasted'
    email = 'test@example.com'

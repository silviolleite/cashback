import datetime
from random import randint

import factory.fuzzy
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User

from cashbackapi.apps.cashback.models import Order, Seller


DEFAULT_PASSWORD = "pass@test"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'john%s' % n)
    first_name = "john"
    last_name = "rambo"
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    password = make_password(DEFAULT_PASSWORD)
    is_active = True


class SellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seller
        django_get_or_create = ('user', 'document')

    user = factory.SubFactory(UserFactory)
    document = ''.join(["{}".format(randint(0, 9)) for num in range(0, 11)])


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = ("seller", "amount", "date")

    seller = factory.SubFactory(SellerFactory)
    code = factory.Sequence(lambda n: 'B-%s' % n)
    amount = factory.fuzzy.FuzzyDecimal(100.0, 1200.0)
    date = factory.LazyFunction(datetime.datetime.now)

import pytest

from cashbackapi.apps.cashback.models import Order

pytestmark = pytest.mark.django_db


def test_cashback_get_queryset(order):
    cashback = Order.cashback_total.filter(seller=order.seller, date__month=order.date.month).get()
    assert cashback["total"] == order.amount

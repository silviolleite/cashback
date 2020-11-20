import pytest

from cashbackapi.apps.cashback.models import APPROVED, SPECIAL_SELLER_DOCUMENT

pytestmark = pytest.mark.django_db


def test_create_special_seller(special_seller):
    assert special_seller.document == SPECIAL_SELLER_DOCUMENT


def test_order_status_for_special_seller(order_special_seller):
    assert order_special_seller.status == APPROVED
    assert order_special_seller.get_status_display() == "Aprovado"
    assert order_special_seller.__str__() == order_special_seller.code

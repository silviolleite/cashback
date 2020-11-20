import pytest
from rest_framework.status import is_success

from cashbackapi.apps.cashback.models import Seller
from cashbackapi.tests.cashback.factories import OrderFactory

pytestmark = pytest.mark.django_db


def test_api_get_orders_is_a_list(auth_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, amount="1000")
    response = auth_client.get("/api/cashback/")
    assert isinstance(response.json(), list)
    assert is_success(response.status_code), str(response.content, "utf-8")


def test_api_get_orders_list_until_1000(auth_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, amount="1000")
    response = auth_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert orders[0]["amount"] == "1000.00"
    assert orders[0]["cashback_percent"] == "10"
    assert orders[0]["cashback_value"] == "100.00"
    assert orders[0]["status"] == "Em Validação"


def test_api_get_orders_list_between_1000_and_1500(auth_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, amount="1500")
    response = auth_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert orders[0]["amount"] == "1500.00"
    assert orders[0]["cashback_percent"] == "15"
    assert orders[0]["cashback_value"] == "225.00"
    assert orders[0]["status"] == "Em Validação"


def test_api_get_orders_list_over_1500(auth_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, amount="1501")
    response = auth_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert orders[0]["amount"] == "1501.00"
    assert orders[0]["cashback_percent"] == "20"
    assert orders[0]["cashback_value"] == "300.20"
    assert orders[0]["status"] == "Em Validação"


def test_api_get_orders_list_length(auth_client):
    seller = Seller.objects.all().first()
    quantity = 20
    OrderFactory.create_batch(quantity, seller=seller)
    response = auth_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert len(orders) == quantity


def test_api_get_orders_list_length_by_month(auth_client):
    seller = Seller.objects.all().first()
    quantity = 20
    OrderFactory.create_batch(quantity, seller=seller)
    OrderFactory(seller=seller, date="2020-01-01")
    response = auth_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert len(orders) == quantity


def test_api_get_orders_list_special_seller_status(auth_special_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller)
    response = auth_special_client.get("/api/cashback/")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert orders[0]["status"] == "Aprovado"


def test_api_get_orders_list_by_month(auth_special_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, date="2020-04-10")
    response = auth_special_client.get("/api/cashback/?month=04")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert len(orders) == 1


def test_api_get_orders_list_by_year(auth_special_client):
    seller = Seller.objects.all().first()
    OrderFactory(seller=seller, date="2020-04-10")
    response = auth_special_client.get("/api/cashback/?year=2019")
    orders = response.json()
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert len(orders) == 0

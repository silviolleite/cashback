import pytest
from rest_framework.authtoken.models import Token

from cashbackapi.apps.cashback.models import SPECIAL_SELLER_DOCUMENT
from cashbackapi.tests.cashback.factories import DEFAULT_PASSWORD, OrderFactory, SellerFactory, UserFactory

from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, seller):
    payload = {
        "username": seller.user.username,
        "password": DEFAULT_PASSWORD
    }
    response = client.post("/api/token/", payload, format='json').json()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response["access"])
    return client


@pytest.fixture
def auth_special_client(client, special_seller):
    payload = {
        "username": special_seller.user.username,
        "password": DEFAULT_PASSWORD
    }
    response = client.post("/api/token/", payload, format='json').json()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response["access"])
    return client


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def seller():
    return SellerFactory()


@pytest.fixture
def special_seller():
    return SellerFactory(document=SPECIAL_SELLER_DOCUMENT)


@pytest.fixture
def order():
    return OrderFactory()


@pytest.fixture
def order_special_seller(special_seller):
    return OrderFactory(seller=special_seller)


@pytest.fixture
def seller_payload():
    return {
        "username": "teste",
        "first_name": "teste",
        "last_name": "teste",
        "email": "teste@teste.com",
        "document": "12345678901",
        "password": "123456"
    }


@pytest.fixture
def seller_payload_response(seller_payload):
    seller_payload_response = seller_payload
    seller_payload_response["password"] = "***********"
    return seller_payload_response


@pytest.fixture
def cashback_amount():
    return {
        'body': {
            'credit': 1193
        },
        'statusCode': 200
    }


@pytest.fixture
def cashback_amount_error():
    return {
        "statusCode": 400,
        "body": {
            "message": "Informe o CPF do revendedor(a)!"
        }
    }

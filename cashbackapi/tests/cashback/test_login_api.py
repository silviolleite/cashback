import pytest
from rest_framework.status import is_client_error, is_success

from cashbackapi.tests.cashback.factories import DEFAULT_PASSWORD

pytestmark = pytest.mark.django_db


def test_api_login_seller(client, seller):
    payload = {
        "username": seller.user.username,
        "password": DEFAULT_PASSWORD
    }
    response = client.post("/api/token/", payload, format='json')
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert "access" in response.json()
    assert "refresh" in response.json()


def test_api_login_seller_password_error(client, seller):
    payload = {
        "username": seller.user.username,
        "password": "wrongpass"
    }
    response = client.post("/api/token/", payload, format='json')
    expected_error = {"detail": "No active account found with the given credentials"}
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_error


def test_api_login_seller_username_error(client, seller):
    payload = {
        "username": "",
        "password": DEFAULT_PASSWORD
    }
    response = client.post("/api/token/", payload, format='json')
    expected_error = {'username': ['Este campo não pode ser em branco.']}
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_error


def test_api_login_seller_invalid_username_error(client, seller):
    payload = {
        "username": "notme",
        "password": DEFAULT_PASSWORD
    }
    response = client.post("/api/token/", payload, format='json')
    expected_error = {"detail": "No active account found with the given credentials"}
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_error

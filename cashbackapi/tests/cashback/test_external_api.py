import pytest
import responses

from rest_framework.status import is_success

from cashbackapi.apps.cashback.external_api import CashbackAPIClient
from cashbackapi.apps.cashback.models import Seller
from cashbackapi.settings import API_TOKEN, API_URL

pytestmark = pytest.mark.django_db


def test_wrong_endpoint():
    cashback_external_api = CashbackAPIClient(
        API_URL,
        API_TOKEN,
    )
    with pytest.raises(ValueError) as cm:
        cashback_external_api.get_url("create")
    assert cm


@responses.activate
def test_api_cashback_amount(auth_client, cashback_amount):
    seller = Seller.objects.all().first()
    responses.add(
        responses.GET,
        "{}v1/cashback?cpf={}".format(API_URL, seller.document),
        json=cashback_amount,
        status=200,
    )
    response = auth_client.get("/api/cashback/amount/")
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert response.json() == cashback_amount


@responses.activate
def test_api_cashback_amount(auth_client, cashback_amount):
    seller = Seller.objects.all().first()
    responses.add(
        responses.GET,
        "{}v1/cashback?cpf={}".format(API_URL, seller.document),
        json=cashback_amount,
        status=200,
    )
    response = auth_client.get("/api/cashback/amount/")
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert response.json() == cashback_amount


@responses.activate
def test_api_cashback_amount_without_document(auth_client, cashback_amount_error):
    seller = Seller.objects.all().first()
    seller.document = ""
    seller.save()
    responses.add(
        responses.GET,
        "{}v1/cashback?cpf={}".format(API_URL, ""),
        json=cashback_amount_error,
        status=200,
    )
    response = auth_client.get("/api/cashback/amount/")
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert response.json() == cashback_amount_error

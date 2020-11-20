import pytest
from rest_framework.status import is_client_error, is_success

pytestmark = pytest.mark.django_db


def test_api_create_seller(client, seller_payload, seller_payload_response):
    response = client.post("/api/seller/register/", seller_payload)
    assert is_success(response.status_code), str(response.content, "utf-8")
    assert response.json() == seller_payload_response


def test_api_create_seller_password_error(client, seller_payload):
    seller_payload["password"] = ""
    expected_response_error = {"password":["Este campo não pode ser em branco."]}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_empty_document_error(client, seller_payload):
    seller_payload["document"] = ""
    expected_response_error = {'document': ['Este campo não pode ser em branco.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_document_not_digit_error(client, seller_payload):
    seller_payload["document"] = "a1234567891"
    expected_response_error = {'document': ['Número de CPF inválido.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_document_max_digit_error(client, seller_payload):
    seller_payload["document"] = "123456789012"
    expected_response_error = {'document': ['Certifique-se de que este campo não tenha mais de 11 caracteres.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_empty_first_name_error(client, seller_payload):
    seller_payload["first_name"] = ""
    expected_response_error = {'first_name': ['Este campo não pode ser em branco.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_empty_last_name_error(client, seller_payload):
    seller_payload["last_name"] = ""
    expected_response_error = {'last_name': ['Este campo não pode ser em branco.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_empty_email_error(client, seller_payload):
    seller_payload["email"] = ""
    expected_response_error = {'email': ['Este campo não pode ser em branco.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_email_format_error(client, seller_payload):
    seller_payload["email"] = "test%test"
    expected_response_error = {'email': ['Insira um endereço de email válido.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_empty_username_error(client, seller_payload):
    seller_payload["username"] = ""
    expected_response_error = {'username': ['Este campo não pode ser em branco.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_username_special_char_error(client, seller_payload):
    seller_payload["username"] = "me%test"
    expected_response_error = {'username': ['Este campo não deve conter caracteres especiais e espaços.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_username_white_space_error(client, seller_payload):
    seller_payload["username"] = "me test"
    expected_response_error = {'username': ['Este campo não deve conter caracteres especiais e espaços.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_username_uppercase_error(client, seller_payload):
    seller_payload["username"] = "Me"
    expected_response_error = {'username': ['Este deve conter apenas caracteres minúsculo.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_username_unique_error(client, seller_payload, seller):
    seller_payload["username"] = seller.user.username
    expected_response_error = {'username': 'Usuário já cadastrado no sistema'}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error


def test_api_create_seller_document_unique_error(client, seller_payload, seller):
    seller_payload["document"] = seller.document
    expected_response_error = {'document': ['seller com este document já existe.']}
    response = client.post("/api/seller/register/", seller_payload)
    assert is_client_error(response.status_code), str(response.content, "utf-8")
    assert response.json() == expected_response_error

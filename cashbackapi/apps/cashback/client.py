from cashbackapi.apps.cashback.external_api import CashbackAPIClient
from cashbackapi.settings import API_TOKEN, API_URL

cashback_external_api = CashbackAPIClient(
    API_URL,
    API_TOKEN,
)

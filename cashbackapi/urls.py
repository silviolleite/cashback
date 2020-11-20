from django.urls import include, path
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('api/', include("cashbackapi.apps.cashback.urls")),
    path('', get_schema_view(
            title="Cashback API",
            description="API for cashback control",
            version="1.0.0"
        ), name='openapi-schema'),
]


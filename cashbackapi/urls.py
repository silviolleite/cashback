from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('api/', include("cashbackapi.apps.cashback.urls")),
]

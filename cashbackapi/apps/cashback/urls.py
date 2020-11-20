from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'seller/register', views.SellerViewSet, basename='seller_register')
router.register(r'cashback', views.OrderViewSet, basename='cashback')

urlpatterns = [
    path('cashback/amount/', views.ExtenalAPIView.as_view(), name='cashback_amount'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls + urlpatterns

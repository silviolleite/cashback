import logging
from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import cashback_external_api
from .models import Order, Seller
from .serializers import OrderSerializer, SellerSerializer

logger = logging.getLogger(__name__)


class SellerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (AllowAny, )


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        today = datetime.today()
        month = self.request.query_params.get('month', today.month)
        year = self.request.query_params.get('year', today.year)
        logger.info(f"Filtering list by: month={month}, year={year}")
        seller = self.request.user.seller
        return Order.objects.filter(seller=seller, date__month=month, date__year=year)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller)


class ExtenalAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        document = request.user.seller.document
        logger.info(f"Calling external API with document={document}")
        response = cashback_external_api.fetch(document)
        logger.debug(f"got response: {response.json()}")
        return Response(response.json())

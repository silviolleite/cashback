import logging

from django.contrib.auth.models import User
from django.db import IntegrityError
from drf_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Order, Seller
from .validators import validate_username

logger = logging.getLogger(__name__)

ORDER_FIELDS = (
    "code",
    "amount",
    "date",
)

ORDER_READ_FIELDS = (
    "status",
    "cashback_percent",
    "cashback_value",
    "created_at",
)

SELLER_FIELDS = (
    'username',
    'first_name',
    'last_name',
    'email',
    'document',
    'password',
)


class SellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', validators=[validate_username])
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password')

    class Meta:
        model = Seller
        fields = SELLER_FIELDS
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        logger.info("Creating a new seller")
        password = validated_data["user"].pop('password')
        user = User(**validated_data["user"])
        user.set_password(password)

        try:
            user.save()
        except IntegrityError:
            error = {'username': 'Usuário já cadastrado no sistema'}
            raise ValidationError(error)

        seller = Seller(user=user, document=validated_data["document"])
        seller.save()
        seller.user.password = "***********"
        logger.info("New seller created with success")
        return seller


class OrderSerializer(FieldsListSerializerMixin, ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    cashback_percent = serializers.SerializerMethodField()
    cashback_value = serializers.SerializerMethodField()

    def get_total(self, obj):
        logger.info(f"Get amount of orders by month for seller={obj.seller}")
        orders = Order.cashback_total.filter(seller=obj.seller, date__month=obj.date.month).get()
        return int(orders["total"])

    def get_cashback_percent(self, obj):
        logger.info(f"Calculate cashback percent for order={obj.code}")
        total = self.get_total(obj)
        logger.debug(f"Caulculate cashback percent with total={total}")
        if total <= 1000:
            cashback_percent = "10"
        elif total <= 1500:
            cashback_percent = "15"
        else:
            cashback_percent = "20"
        logger.debug(f"The cashback percent for total={total} is {cashback_percent}")
        return cashback_percent

    def get_cashback_value(self, obj):
        logger.info(f"Getting cashback value for order={obj.code}")
        percent = self.get_cashback_percent(obj)
        cashback_value = format(int(percent) * obj.amount / 100, '.2f')
        logger.debug(f"Calculated the cashback value, order_amount={obj.amount}, "
                     f"percent={percent}, cashback_value={cashback_value}")
        return cashback_value

    class Meta:
        model = Order
        fields = ORDER_FIELDS + ORDER_READ_FIELDS
        read_only_fields = ORDER_READ_FIELDS

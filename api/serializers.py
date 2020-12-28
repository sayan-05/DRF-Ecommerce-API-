from rest_framework import serializers
from .models import BoughtItem, ProductInfo, OrderItem
from rest_framework_simplejwt.serializers import api_settings
from django.contrib.auth.models import User


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, object):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(object)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'username', 'password')


class GetFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser')


class GetUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class OrderItemSerializer(serializers.ModelSerializer):

    item = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'ordered', 'quantity', 'user', 'item', 'proceed']


class GetOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'user']


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(read_only=False)
    user_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity', 'user_id', 'proceed']


class OrderItemDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False)
    user_id = serializers.IntegerField(read_only=False)


class BoughtItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoughtItem
        fields = ['user']


class BoughtItemGetSerializer(serializers.ModelSerializer):

    item = ProductInfoSerializer()

    class Meta:
        model = BoughtItem
        fields = '__all__'


from rest_framework import serializers
from . import models
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'password','first_name','last_name']

    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields =['name','category','description','price','quantity','is_out_of_stock'] 

class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = []

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id','password','email','username','first_name','last_name','is_active','is_staff','is_superuser','date_joined','phone']

class PurchaseListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name.username', read_only=True)
    productname = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = models.Purchase
        fields = '__all__'

class PaymentListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name.username', read_only=True)
    productname = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = models.Purchase
        fields = ['total_price','productname','username']



# user ---------------------------------------------------------------------------

class CartItemSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = models.CartItem
        fields = ['id', 'cart', 'productname', 'quantity']

class BuyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        fields = ['name','product','quantity']
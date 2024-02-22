from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from . import serializers 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import models
from rest_framework.views import APIView



# Create your views here.
class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'phone':user.phone
        })
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'is_staff': user.is_staff,
                'is_admin': user.is_superuser
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


#admin start--------------------------------------------------------------

class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['quantity'] == 0:
                serializer.validated_data['is_out_of_stock'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def get(self, request, format=None):
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Product.objects.all()

class ProductDelete(generics.DestroyAPIView):
    serializer_class = serializers.ProductDeleteSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Product.objects.all()
    
class ProductOutOfStock(APIView):
    def get(self, request, format=None):
        products = models.Product.objects.filter(is_out_of_stock = True)
        serializer = serializers.ProductSerializer(products, many = True)
        return Response(serializer.data)
    
class UserList(APIView):
    def get(self, request, format=None):
        users = models.CustomUser.objects.all()
        serializer = serializers.UserListSerializer(users, many = True)
        return Response(serializer.data)
    
class PurchaseList(APIView):
    def get(self, request, format=None):
        purchases = models.Purchase.objects.all()
        serializer = serializers.PurchaseListSerializer(purchases, many = True)
        return Response(serializer.data)

class PaymentList(APIView):
    def get(self, request, format=None):
        payments = models.Purchase.objects.all()
        serializer = serializers.PaymentListSerializer(payments, many = True)
        return Response(serializer.data)

#user start--------------------------------------------------------------- 

class DesplayProducts(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Product.objects.all()
        return queryset

class ListOffers(generics.ListAPIView):
    serializer_class = serializers.ListOfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Offer.objects.all()
        return queryset

class AddToCart(generics.CreateAPIView):
    serializer_class = serializers.CartItemSerializer

    def post(self, request, *args, **kwargs):     
        user = request.user
        product_id = self.kwargs.get('product_id')
        products = get_object_or_404(models.Product, pk=product_id)
        quantity = self.kwargs.get('quantity')
        print('------------------------------------')
        print(products)
        if quantity <= products.quantity:
            if not product_id:
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                cart = models.Cart.objects.get(user=user)
            except models.Cart.DoesNotExist:
                cart = models.Cart.objects.create(user=user)
            product = models.Product.objects.get(pk=product_id)  
            try:
                cart_item = models.CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.save()
            except models.CartItem.DoesNotExist:
                cart_item = models.CartItem.objects.create(cart=cart, product=product, quantity=quantity)

            serializer = self.get_serializer(cart_item)
        else:
            return Response({'error':'That much product not available'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CartItemsListview(generics.ListAPIView):
    serializer_class=serializers.CartItemSerializer
    queryset=models.CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        query=models.CartItem.objects.filter(cart__user=user)
        return query
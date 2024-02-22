from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RegistrationView.as_view(),name='RegistrationView'),#add a new user into db
    path('login/',views.UserLoginView.as_view(),name='UserLoginView'),#login
    # admin------------------------------------------------------------------------
    path('ProductAPIView/',views.ProductAPIView.as_view(),name='ProductAPIView'),#Create and list product
    path('ProductUpdate/<int:pk>/',views.ProductUpdate.as_view(),name='ProductUpdate'),#update the product info by id
    path('ProductDelete/<int:pk>/',views.ProductDelete.as_view(),name='ProductDelete'),#delete product by id
    path('ProductOutOfStock/',views.ProductOutOfStock.as_view(),name='ProductOutOfStock'),#product list of outof stock
    path('UserList/',views.UserList.as_view(),name='UserList'),#
    path('PurchaseList/',views.PurchaseList.as_view(),name='PurchaseList'),
    path('PaymentList/',views.PaymentList.as_view(),name='PaymentList'),
    # user-------------------------------------------------------------------------
    path('DesplayProducts/',views.DesplayProducts.as_view(),name='DesplayProducts'),
    path('AddToCart/<int:product_id>/<int:quantity>/',views.AddToCart.as_view(),name='AddToCart'),
    path('CartItemsListview/',views.CartItemsListview.as_view(),name='CartItemsListview'),
    path('ListOffers/',views.ListOffers.as_view(),name='ListOffers'),
    ]
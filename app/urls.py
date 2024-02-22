from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RegistrationView.as_view(),name='RegistrationView'),
    path('login/',views.UserLoginView.as_view(),name='UserLoginView'),
    # admin------------------------------------------------------------------------
    path('ProductAPIView/',views.ProductAPIView.as_view(),name='ProductAPIView'),
    path('ProductUpdate/<int:pk>/',views.ProductUpdate.as_view(),name='ProductUpdate'),
    path('ProductDelete/<int:pk>/',views.ProductDelete.as_view(),name='ProductDelete'),
    path('ProductOutOfStock/',views.ProductOutOfStock.as_view(),name='ProductOutOfStock'),
    path('UserList/',views.UserList.as_view(),name='UserList'),
    path('PurchaseList/',views.PurchaseList.as_view(),name='PurchaseList'),
    path('PaymentList/',views.PaymentList.as_view(),name='PaymentList'),
    # user-------------------------------------------------------------------------
    path('DesplayProducts/',views.DesplayProducts.as_view(),name='DesplayProducts'),
    path('AddToCart/<int:product_id>/<int:quantity>/',views.AddToCart.as_view(),name='AddToCart'),
    path('BuyProduct/<int:product_id>/<int:quantity>/',views.AddToCart.as_view(),name='AddToCart'),
    ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('order/',views.Orders.as_view(), name='order'),
    path('signup/',views.signup.as_view(), name='signup'),
    path('login/',views.login.as_view(), name='login'),
    path('logout/',views.logout,name='logout'),
    path('cart/',views.Cart.as_view(),name='cart'),
    path('chackout/',views.Checkout.as_view(),name='chack-out'),
    
]

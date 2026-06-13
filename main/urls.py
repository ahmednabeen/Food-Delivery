from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    path('browse/', views.browse, name='browse'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('food/<slug:slug>/', views.food_detail, name='food_detail'),
    path('food/<slug:slug>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/<slug:slug>/update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]

# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stock/<str:symbol>/', views.get_stock_info),
    path('register/', views.register),
    path('login/', views.login),
    path('api-token-auth/', views.obtain_auth_token),
    path('watchlist/', views.get_watchlist),
    path('watchlist/add/', views.add_to_watchlist),
    path('stock/<str:symbol>/', views.get_stock_info),
]

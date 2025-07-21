# core/urls.py

from django.urls import path
from .views import LandingView, ThanksView, OrdersListView, OrderDetailView, service_create_view

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('services/create/', service_create_view, name='service_create'),
]
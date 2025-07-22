from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LandingView, ThanksView, OrdersListView, OrderDetailView, ServiceCreateView

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from core.views import masters_detail, thanks

urlpatterns = [
    path('masters/<int:master_id>/', masters_detail),
    path('thanks/', thanks),
]
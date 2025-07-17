from django.contrib import admin
from django.urls import path
from core.views import main, masters_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('masters/<int:master_id>/', masters_detail),
]

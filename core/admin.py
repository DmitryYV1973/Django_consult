from django.contrib import admin
from .models import Master, Service, Order, Review

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone')
    filter_horizontal = ('services',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular', 'order')
    list_editable = ('price', 'order', 'is_popular')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone', 'status', 'appointment_date')
    list_filter = ('status', 'appointment_date')
    search_fields = ('client_name', 'phone')
    date_hierarchy = 'appointment_date'
    filter_horizontal = ('services',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')
    date_hierarchy = 'created_at'
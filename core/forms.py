# core/forms.py
from django import forms
from .models import Order, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'photo', 'rating']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'client_name',
            'phone',
            'comment',
            'master',
            'services',
            'appointment_date',
        ]
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
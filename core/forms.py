from django import forms
from .models import Order, Review
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


from django import forms
from .models import Review, Master

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'photo', 'rating', 'master']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ваш отзыв'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'client_name': 'Ваше имя',
            'text': 'Ваш отзыв',
            'photo': 'Прикрепить фотографию',
            'rating': 'Оценка (от 1 до 5)',
            'master': 'Мастер, которого оцениваете',
        }
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'comment', 'master', 'services', 'appointment_date']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
                'required': 'required'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация'
            }),
            'master': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'appointment_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'required': 'required'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        appointment_date = cleaned_data.get('appointment_date')

        # Проверяем, что выбран мастер
        if not master:
            self.add_error('master', 'Пожалуйста, выберите мастера.')

        # Проверяем, что выбрана хотя бы одна услуга
        if not services:
            self.add_error('services', 'Пожалуйста, выберите хотя бы одну услугу.')

        # Проверяем, что дата в будущем
        if appointment_date and appointment_date < timezone.now():
            self.add_error('appointment_date', 'Выберите время в будущем.')

        return cleaned_data

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        
        if not appointment_date:
            raise ValidationError('Это поле обязательно для заполнения.')
            
        # Проверяем, что дата не в прошлом
        if appointment_date < timezone.now():
            raise ValidationError('Дата записи не может быть в прошлом.')
            
        # Проверяем рабочие часы (например, с 9:00 до 20:00)
        hour = appointment_date.hour
        if hour < 9 or hour >= 20:
            raise ValidationError('Запись возможна только с 9:00 до 20:00.')
            
        # Проверяем, что это не выходной (например, воскресенье)
        if appointment_date.weekday() == 6:  # 6 - воскресенье
            raise ValidationError('В воскресенье мы не работаем.')
        
        # Проверяем доступность выбранного времени
        master = self.cleaned_data.get('master')
        
        if appointment_date and master:
            # Проверяем, нет ли уже записи на это время к этому мастеру
            existing_appointments = Order.objects.filter(
                master=master,
                appointment_date__range=(
                    appointment_date - timezone.timedelta(minutes=30),
                    appointment_date + timezone.timedelta(minutes=30)
                ),
                status__in=['approved', 'completed']
            )
            
            if existing_appointments.exists():
                raise ValidationError(
                    'Выбранное время уже занято. Пожалуйста, выберите другое время.'
                )
        
        return appointment_date


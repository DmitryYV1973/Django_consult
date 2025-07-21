from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to='services/', verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        indexes = [
            models.Index(fields=['price']),  # Одинарный индекс по цене
            models.Index(fields=['is_popular']),  # Одинарный индекс по популярности
            models.Index(fields=['price', 'duration'])  # Составной индекс по цене и продолжительности
        ]
        
        verbose_name = "Услуга"
        verbose_name_plural = "Список услуг"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    experience = models.PositiveIntegerField(
        verbose_name="Стаж работы", 
        help_text="Опыт работы в годах"
    )
    services = models.ManyToManyField(
        Service,
        related_name="masters",
        verbose_name="Услуги"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Список мастеров"
        ordering = ['-is_active', 'name']

    def __str__(self):
        return f"{self.name} (стаж: {self.experience} лет)"



class Order(models.Model):
    STATUS_CHOICES = [
        ('not_approved', 'Не подтверждён'),
        ('approved', 'Подтвержден'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменён'),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="not_approved", 
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey(
        Master, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Мастер"
    )
    services = models.ManyToManyField(
        Service, 
        related_name="orders", 
        verbose_name="Услуги"
    )
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name}"
    
    def get_total_price(self):
        return sum(service.price for service in self.services.all())

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Имя клиента"
    )
    master = models.ForeignKey(
        Master, 
        on_delete=models.CASCADE, 
        verbose_name="Мастер"
    )
    photo = models.ImageField(
        upload_to="reviews/", 
        blank=True, 
        null=True, 
        verbose_name="Фотография"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.client_name} ({self.get_rating_display()})"
    
    def get_rating_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
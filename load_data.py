import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barbershop.settings")
django.setup()

from core.models import Master, Service, Order
from core.data import masters, services, orders

# Загрузка услуг
for service_data in services:
    Service.objects.get_or_create(
        name=service_data["name"],
        defaults={
            "description": "Описание отсутствует",  # или укажите актуальное описание
            "price": service_data["price"],
            "duration": service_data["duration"],
            "is_popular": False,
            "order": 0,
            "image": None,
        }
    )

# Загрузка мастеров
for master_data in masters:
    Master.objects.get_or_create(
        id=master_data["id"],
        defaults={
            "name": master_data["name"],
            "phone": master_data.get("phone", ""),
            "address": master_data.get("address", ""),
            "experience": master_data.get("experience", 0),
            "is_active": master_data.get("is_active", True),
        }
    )

# Загрузка заказов
for order_data in orders:
    master = Master.objects.get(id=order_data["master_id"])
    service_objects = Service.objects.filter(name__in=order_data["services"])

    Order.objects.get_or_create(
        id=order_data["id"],
        defaults={
            "client_name": order_data["client_name"],
            "phone": order_data.get("phone", ""),
            "comment": order_data.get("comment", ""),
            "status": order_data["status"],
            "appointment_date": order_data["date"],
            "master": master,
        }
    )[0].services.set(service_objects)

print("✅ Данные успешно загружены")
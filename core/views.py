from django.shortcuts import render, redirect
from .models import Review, Service, Master, Order
from .forms import ReviewForm, OrderForm
from .data import *


def landing(request):
    services = Service.objects.all()
    masters = Master.objects.filter(is_active=True)
    published_reviews = Review.objects.filter(is_published=True)
    success = False  # Флаг для уведомления об успешной отправке

    form = ReviewForm()  # Инициализируем форму отзыва
    order_form = OrderForm()  # Инициализируем форму заказа

    if request.method == "POST":
        if "submit_review" in request.POST:
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.master_id = request.POST.get("master_id")
                review.is_published = False
                review.save()
                return redirect('landing')
        elif "submit_order" in request.POST:
            order_form = OrderForm(request.POST)  # Переопределяем форму заказа с данными из POST
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.status = 'not_approved'
                order.save()
                order_form.save_m2m()
                success = True  # Устанавливаем флаг в True при успешной отправке
            else:
                # Форма невалидна, обрабатываем ошибки
                pass

    context = {
        'services': services,
        'masters': masters,
        'reviews': published_reviews,
        'form': form,
        'order_form': order_form,
        'success': success,  # Передаем флаг в контекст
    }
    return render(request, 'landing.html', context)


def thanks(request):
    return render(request, 'core/thanks.html')


def orders_list(request):
    context = {
        'orders': orders
    }
    return render(request, 'core/orders_list.html', context)


def order_detail(request, order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    master = next((m for m in masters if m['id'] == order['master_id']), None) if order else None
    
    context = {
        'order': order,
        'master': master
    }
    return render(request, 'core/order_detail.html', context)


def test(request):
    return render(request, 'core/test.html', TEST_CONTEXT)
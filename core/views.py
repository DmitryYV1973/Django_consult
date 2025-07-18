from django.shortcuts import render
from django.http import HttpResponse
from .data import *


def landing(request):
    context = {
        'masters': masters,
        'services': services
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
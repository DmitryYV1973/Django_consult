from django.shortcuts import render
from django.http import HttpResponse


masters = [
    {"id": 1, "name": "Иван Петров"},
    {"id": 2, "name": "Анна Смирнова"},
    {"id": 3, "name": "Сергей Иванов"},
    {"id": 4, "name": "Елена Козлова"},
    {"id": 5, "name": "Дмитрий Соколов"}
]


def main(request):
    return HttpResponse("Добро пожаловать в наш барбершоп!")


def masters_detail(request, master_id):
    try:
        master = [master for master in masters if master["id"] == master_id][0]
    except IndexError:
        return HttpResponse("Мастер не найден")
    return HttpResponse(f"<h1>{master['name']}</h1>")
        

def thanks(request):
    masters_count = len(masters)
    
    context = {
        'masters_count': masters_count,
    }
    return render(request, 'thanks.html', context)
def navbar_links(request):
    return {
        'navbar_links': [
            {'name': 'О нас', 'url': '#about'},
            {'name': 'Услуги', 'url': '#services'},
            {'name': 'Мастера', 'url': '#masters'},
            {'name': 'Запись', 'url': '#booking'},
        ]
    }
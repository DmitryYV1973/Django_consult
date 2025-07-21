from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Review, Order, Master, Service
from .forms import OrderForm, ReviewForm
from django.db.models import Q

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib import messages

class LandingView(FormView):
    template_name = 'landing.html'
    form_class = ReviewForm
    order_form_class = OrderForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['masters'] = Master.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(is_published=True)
        context['order_form'] = self.order_form_class()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        if "submit_order" in request.POST:
            order_form = self.order_form_class(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.status = 'not_approved'
                order.save()
                order_form.save_m2m()
                return HttpResponseRedirect(reverse_lazy('thanks'))
            else:
                return self.render_to_response(self.get_context_data(order_form=order_form))
        elif "submit_review" in request.POST:
            review_form = self.form_class(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                master_id = request.POST.get("master")
                try:
                    master = Master.objects.get(pk=master_id)
                    review.master = master
                    review.is_published = True  # Устанавливаем флаг публикации
                    review.save()
                    messages.success(request, "Ваш отзыв опубликован.")
                    return redirect('landing')
                except Master.DoesNotExist:
                    messages.error(request, "Пожалуйста, выберите мастера для отзыва.")
                    return self.render_to_response(self.get_context_data(form=review_form))
            else:
                return self.render_to_response(self.get_context_data(form=review_form))

class ThanksView(TemplateView):
    template_name = 'core/thanks.html'

class OrdersListView(ListView):
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')

        # Получаем параметры GET-запроса
        search_text = self.request.GET.get('search_text', '')
        search_by_client = self.request.GET.get('search_by_client', 'on') == 'on'
        search_by_phone = self.request.GET.get('search_by_phone', 'off') == 'on'
        search_by_comment = self.request.GET.get('search_by_comment', 'off') == 'on'

        if search_text:
            q_objects = Q()
            if search_by_client:
                q_objects |= Q(client_name__icontains=search_text)
            if search_by_phone:
                q_objects |= Q(phone__icontains=search_text)
            if search_by_comment:
                q_objects |= Q(comment__icontains=search_text)
            queryset = queryset.filter(q_objects)

        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
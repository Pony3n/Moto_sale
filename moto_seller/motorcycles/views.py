from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .models import Motorcycle
from .forms import MotorcyclesSearchForm


def show_main(request):
    """
    Отображает главную страницу со списком всех мотоциклов
    """
    motorcycles = Motorcycle.objects.all()
    form = MotorcyclesSearchForm(request.GET)
    page = request.GET.get('page', 1)

    paginator = Paginator(motorcycles, 6)  # 10 объектов на странице
    try:
        motorcycles = paginator.page(page)
    except PageNotAnInteger:
        motorcycles = paginator.page(1)
    except EmptyPage:
        motorcycles = paginator.page(paginator.num_pages)

    context = {
        'motorcycles': motorcycles,
        'form': form
    }
    return render(request, 'motorcycles/index.html', context)


def motorcycle_search(request):
    """
    Отображает форму для поиска конкретных моделей.
    В случае отсутствия совпадений, выводит соответствующее сообщение.
    В случае передачи пустой строки, возвращает на главную страницу.
    """
    search_query = None
    motorcycles = None
    page = request.GET.get('page', 1)

    if request.method == 'GET':
        form = MotorcyclesSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']

            filters = {
                'date_of_issue__gte': form.cleaned_data.get('min_date_of_issue'),
                'date_of_issue__lte': form.cleaned_data.get('max_date_of_issue'),
                'moto_type': form.cleaned_data.get('moto_type') if form.cleaned_data.get('moto_type') else None,
                'price__gte': form.cleaned_data.get('min_price'),
                'price__lte': form.cleaned_data.get('max_price'),
            }

            filters = {key: value for key, value in filters.items() if value is not None}


            print(f'Filters: {filters}')
            if search_query or filters:
                motorcycles = Motorcycle.objects.filter(model_name__icontains=search_query, **filters)

                paginator = Paginator(motorcycles, 6)
                print(f'Page: {page}')

                try:
                    motorcycles = paginator.page(page)
                except PageNotAnInteger:
                    motorcycles = paginator.page(1)
                except EmptyPage:
                    motorcycles = paginator.page(paginator.num_pages)

        context = {
            'motorcycles': motorcycles,
            'search_query': search_query,
            'form': form,
            'no_result_message': "Совпадений не найдено" if motorcycles is not None and not motorcycles.object_list else None,
        }

        template = 'motorcycles/search_list.html' if motorcycles is not None else 'motorcycles/index.html'
        return render(request, template, context)


def show_about(request):
    return render(request, 'motorcycles/about.html')


def show_contact(request):
    return render(request, 'motorcycles/contact.html')


class MotorcycleDetailView(View):
    template_name = "motorcycles/motorcycle_detail.html"

    def get(self, request, *args, **kwargs):
        moto = Motorcycle.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name, {"moto": moto})
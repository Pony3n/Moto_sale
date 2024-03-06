from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from .models import Motorcycle
from .forms import MotorcyclesSearchForm


def show_main(request):
    """
    Отображает главную страницу со списком всех мотоциклов
    """
    motorcycles = Motorcycle.objects.all()
    form = MotorcyclesSearchForm(request.GET)

    context = {
        'motorcycles': motorcycles,
        'form': form
    }
    return render(request, 'motorcycles/index.html', context)


def motorcycle_search(request):
    """
    Отображает форму для поиска конкретных моделей. В случае отсутствия совпадений, выводит соответствующее сообщение.
    В случае передачи пустой строки, возвращает на главную страницу.
    """
    search_query = None
    if request.method == 'GET':
        form = MotorcyclesSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            if search_query != None:
                motorcycles = Motorcycle.objects.filter(model_name__icontains=search_query)
                if motorcycles.exists():
                    context = {
                        'motorcycles': motorcycles,
                        'search_query': search_query,
                        'form': form,
                    }
                    return render(request, 'motorcycles/search_list.html', context)
                else:
                    no_result_message = "Совпадений не найдено"
                    context = {
                        'motorcycles': motorcycles,
                        'form': form,
                        'no_result_message': no_result_message,
                    }
                    return render(request, 'motorcycles/search_list.html', context)

    context = {
        'search_query': search_query,
        'form': MotorcyclesSearchForm(),
    }

    return render(request, 'motorcycles/index.html', context)


def show_about(request):
    return render(request, 'motorcycles/about.html')


def show_contact(request):
    return render(request, 'motorcycles/contact.html')


class MotorcycleDetailView(View):
    template_name = "motorcycles/motorcycle_detail.html"

    def get(self, request, *args, **kwargs):
        moto = Motorcycle.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name, {"moto": moto})
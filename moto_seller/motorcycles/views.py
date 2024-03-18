from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from moto_cart.models import CartItem, Cart
from .models import Motorcycle
from .forms import MotorcyclesSearchForm, MotoAddToCartForm


class MainView(View):
    """
    Отображает главную страницу со списком всех мотоциклов
    """
    items_per_page = 6
    template_name = 'motorcycles/index.html'

    def get(self, request, *args, **kwargs):
        motorcycles = Motorcycle.objects.all()
        form = MotorcyclesSearchForm(request.GET)
        page = request.GET.get('page', 1)

        paginator = Paginator(motorcycles, self.items_per_page)
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

        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     form = MotoAddToCartForm(request.POST)
    #     if form.is_valid():
    #         motorcycle = get_object_or_404(Motorcycle, pk=form.cleaned_data['motorcycle_id'])
    #         if request.user.is_authenticated and hasattr(request.user, 'cart'):
    #             cart_item, created = CartItem.objects.get_or_create(cart=request.user.cart, motorcycle=motorcycle)
    #             if not created:
    #                 cart_item.quantity += form.cleaned_data['quantity']
    #                 cart_item.save()
    #
    #     return redirect('motorcycles:show_main')


class MotoSearch(View):
    """
    Отображает форму для поиска конкретных моделей.
    В случае отсутствия совпадений, выводит соответствующее сообщение.
    В случае передачи пустой строки, возвращает на главную страницу.
    """
    search_query = None
    motorcycles = None

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
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
            if self.search_query or filters:
                motorcycles = Motorcycle.objects.filter(model_name__icontains=search_query, **filters)

                paginator = Paginator(motorcycles, 6)
                print(f'Page: {page}')

                try:
                    self.motorcycles = paginator.page(page)
                except PageNotAnInteger:
                    self.motorcycles = paginator.page(1)
                except EmptyPage:
                    self.motorcycles = paginator.page(paginator.num_pages)

        context = {
            'motorcycles': self.motorcycles,
            'search_query': self.search_query,
            'form': form,
            'no_result_message': "Совпадений не найдено" if self.motorcycles is not None
                                                            and not self.motorcycles.object_list else None,
        }

        template = 'motorcycles/search_list.html' if self.motorcycles is not None else 'motorcycles/index.html'
        return render(request, template, context)


def show_about(request):
    return render(request, 'motorcycles/about.html')


def show_contact(request):
    return render(request, 'motorcycles/contact.html')


class MotorcycleDetailView(View):
    template_name = "motorcycles/motorcycle_detail.html"

    def get(self, request, *args, **kwargs):
        moto = Motorcycle.objects.get(pk=self.kwargs['pk'])
        form = MotoAddToCartForm(initial={'motorcycle': moto.id})
        auth_message = "Чтобы добавить товар в корзину, пожалуйста, войдите или зарегистрируйтесь."

        context = {
            'moto': moto,
            'form': form,
            "auth_message": auth_message
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = MotoAddToCartForm(request.POST)
        if form.is_valid():
            print('Форма прошла валидацию')
            print(f"Количество: {form.cleaned_data['quantity']}")
            motorcycle = get_object_or_404(Motorcycle, pk=self.kwargs['pk'])

            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
                print('Корзина создана')

                print('Юзер авторизован')
                cart_item, created = CartItem.objects.get_or_create(cart=cart, motorcycle=motorcycle)

                print('Корзина пользователя создана')
                if not created:
                    cart_item.quantity += form.cleaned_data['quantity']
                    cart_item.save()
                else:
                    cart_item.quantity = form.cleaned_data['quantity']
                    cart_item.save()
            else:
                return render(request, self.template_name, {"moto": motorcycle})
        return redirect('motorcycles:motorcycle_detail', pk=self.kwargs['pk'])

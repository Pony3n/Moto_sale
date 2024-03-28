import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages

from motorcycles.models import Motorcycle
from .forms import MotoUserCreationForm, MotoUserLoginForm, MotoUserCreateMotorcycleForm


logger = logging.getLogger(__name__)


class MotoUserRegistrationView(CreateView):
    """
    Представление отвечающее за регистрацию пользователя.
    В случае прохождения валидации, пользователь отправляется на страницу собственного профиля.
    """
    form_class = MotoUserCreationForm
    template_name = 'moto_user/register.html'
    success_url = reverse_lazy('profile', kwargs={'pk': 1})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('moto_user:profile', kwargs={'pk': self.object.pk})


class MotoUserProfileView(LoginRequiredMixin, View):
    """
    Представление отвечающее за страницу пользователя.
    Помимо информации о самом пользователе, выводит и список лотов, которые создал пользователь.
    Так же предоставляет функционал по добавлению лота.
    """
    template_name = 'moto_user/profile.html'

    def get(self, request, *args, **kwargs):
        creator = request.user
        motorcycles = Motorcycle.objects.filter(creator=creator)
        context = {
            'motorcycles': motorcycles,
            'user': creator
        }
        return render(request, self.template_name, context)


class MotoUserLogoutView(LogoutView):
    """
    Представление отвечающее за выход пользователя из аккаунта.
    В случае выхода, отправляет пользователя на главную страницу.
    """
    next_page = reverse_lazy('motorcycles:show_main')

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'Пользователь {request.user} выходит из системы')

        response = super().dispatch(request, *args, **kwargs)

        messages.success(request, 'Вы успешно вышли')
        return response


class MotoUserLoginView(LoginView):
    """
    Представление отвечающее за авторизацию пользователя.
    В случае успешной авторизации - отправляет пользователя на страницу его профиля.
    """
    template_name = 'moto_user/login.html'
    form_class = MotoUserLoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.get_user():
            logger.info('Пользователь зашел')
            return redirect('moto_user:profile', pk=form.get_user().pk)
        return response


class MotoUserCreateMotorcycle(CreateView):
    """
    Представление отвечающее за создание лота мотоцикла пользователем.
    В случае успешного создания, отправляет пользователя на страницу профиля.
    """
    model = Motorcycle
    template_name = 'moto_user/user_create_motorcycle.html'
    form_class = MotoUserCreateMotorcycleForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('moto_user:profile', kwargs={'pk': self.request.user.pk})


class MotoUserUpdateMotorcycle(UpdateView):
    model = Motorcycle
    template_name = 'moto_user/user_update_motorcycle.html'
    form_class = MotoUserCreateMotorcycleForm

    def get_success_url(self):
        return reverse_lazy('moto_user:profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        try:
            moto = Motorcycle.objects.get(pk=self.kwargs['pk'])
            return moto
        except Motorcycle.DoesNotExist:
            return None

    def dispatch(self, request, *args, **kwargs):
        motorcycle = self.get_object()
        if motorcycle is None or motorcycle.creator != request.user:
            return redirect(reverse_lazy('moto_user:profile', kwargs={'pk': self.request.user.pk}))
        return super().dispatch(request, *args, **kwargs)


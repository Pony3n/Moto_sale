from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .forms import MotoUserCreationForm


class MotoRegistrationView(CreateView):
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
    template_name = 'moto_user/profile.html'

    def get(self, request, *args, **kwargs):
        context = {'user': request.user}
        return render(request, self.template_name, context)

from django.shortcuts import render
from django.views import View

from .models import Motorcycle

def show_main(request):
    motorcycles = Motorcycle.objects.all()
    return render(request, 'motorcycles/index.html', {"motorcycles": motorcycles})

def show_about(request):
    return render(request, 'motorcycles/about.html')

def show_contact(request):
    return render(request, 'motorcycles/contact.html')

class MotorcycleDetailView(View):
    template_name = "motorcycles/motorcycle_detail_view.html"

    def get(self, request, *args, **kwargs):
        moto = Motorcycle.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name, {"moto": moto})
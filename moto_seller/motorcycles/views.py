from django.shortcuts import render

from .models import Motorcycle

def show_main(request):
    motorcycles = Motorcycle.objects.all()
    return render(request, 'motorcycles/index.html', {"motorcycles": motorcycles})
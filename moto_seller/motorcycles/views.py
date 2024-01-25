from django.shortcuts import render

from .models import Motorcycle

def show_main(request):
    motorcycles = Motorcycle.objects.all()
    return render(request, 'motorcycles/index.html', {"motorcycles": motorcycles})

def show_about(request):
    return render(request, 'motorcycles/about.html')

def show_contact(request):
    return render(request, 'motorcycles/contact.html')
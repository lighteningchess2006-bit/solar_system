from django.shortcuts import render

def home(request):
    return render(request, 'learning/home.html')


def science(request):
    return render(request, 'learning/science.html')

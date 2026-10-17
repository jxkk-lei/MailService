from django.shortcuts import render


def index(request):
    return render(request, "homepage/index.html")


def not_found(request, exception=None):
    return render(request, "404.html", status=404)
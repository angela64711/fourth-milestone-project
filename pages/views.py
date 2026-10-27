from django.shortcuts import render


def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def retail(request):
    return render(request, "pages/retail.html")

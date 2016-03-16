
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView


def index(request):
    whom = getattr(request, "whom", None)
    return render(request, "index.html", {"whom": whom})

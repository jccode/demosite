
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView


def index(request):
    whom = getattr(request, "whom", None)
    return render(request, "index.html", {"whom": whom})

def register_success(request, username):
    domain_may_with_port = request.META.get("HTTP_HOST") or request.META.get("SERVER_NAME")
    schema = "http" if not request.is_secure() else "https"
    url = "{0}://{1}.{2}".format(schema, username, domain_may_with_port)
    return render(request, "register_success.html", {"url": url})

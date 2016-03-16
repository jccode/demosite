from django.contrib import admin
from subdomain.models import Subdomain

# Register your models here.

class SubdomainAdmin(admin.ModelAdmin):
    list_display = ("name", "url", )


admin.site.register(Subdomain, SubdomainAdmin)
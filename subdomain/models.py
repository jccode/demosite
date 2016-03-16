from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Subdomain(models.Model):
    """
    A model for managing subdomains and the URLs to which they redirect
    """
    name = models.SlugField(max_length=200, unique=True)
    url = models.CharField(max_length=400, verbose_name="URL")

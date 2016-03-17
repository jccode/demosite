from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from subdomain.models import Subdomain
from django.http.response import HttpResponseRedirect
from demosite import urls as frontend_urls

class RedirectMiddleware(object):
    """
    Middleware class that redirect non "www" subdomain request to a specfied URL
    """

    def process_request(self, request):
        """
        Returns an HTTP redirect response for requests including non-"www" subdomains
        :param request:
        :return:
        """
        schema = "http" if not request.is_secure() else "https"
        path = request.get_full_path()
        domain_may_with_port = request.META.get("HTTP_HOST") or request.META.get("SERVER_NAME")

        domain_seprated = domain_may_with_port.split(":")
        port = None
        if len(domain_seprated) > 1:
            domain = domain_seprated[0]
            port = domain_seprated[1]
        else:
            domain = domain_may_with_port

        pieces = domain.split(".")
        subdomain = pieces[0] # join all but primary domain
        default_domain = Site.objects.get(id=settings.SITE_ID).domain
        if domain in {default_domain, "localhost", "127.0.0.1"}:
            return None
        try:
            route = Subdomain.objects.get(name=subdomain).url
        except Subdomain.DoesNotExist:
            route = path

        url = "{0}://{1}{2}".format(schema, default_domain+":"+port if port else default_domain, route)
        print "Redirect to %s" % url
        return HttpResponseRedirect(url)



class AccountMiddleware(object):
    """
    Middleware class that inject account information for non "www" subdomain request
    """

    def process_request(self, request):
        schema = "http" if not request.is_secure() else "https"
        path = request.get_full_path()
        domain_may_with_port = request.META["HTTP_HOST"]

        domain_seprated = domain_may_with_port.split(":")
        port = None
        if len(domain_seprated) > 1:
            domain = domain_seprated[0]
            port = domain_seprated[1]
        else:
            domain = domain_may_with_port

        pieces = domain.split(".")
        subdomain = pieces[0]

        default_domain = Site.objects.get(id=settings.SITE_ID).domain
        redirect_path = "{0}://{1}{2}".format(schema, default_domain+":"+port if port else default_domain, path)
        if domain in {default_domain, "localhost", "127.0.0.1"}:
            return None
        try:
            resolve(path)
        except Resolver404:
            try:
                # The slashes are not being appended before getting here
                resolve(u"{0}/".format(path))
            except Resolver404:
                return redirect(redirect_path)
        try:
            user = User.objects.get(username=subdomain)
        except User.DoesNotExist:
            return redirect(redirect_path)
        request.whom = user
        return None




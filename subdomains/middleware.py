import logging
import operator
import re

from django.conf import settings
from django.utils.cache import patch_vary_headers

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

UNSET = object()


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class SubdomainMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``subdomain`` attribute to the current request.
    """
    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.

        Take the left most part of the URL and consider it the subdomain
        """

        host = request.get_host()
        
        if len(host.split('.')) < 3:
            request.subdomain = None
        else:
            pattern = r'^(?P<subdomain>[^\.]*)'
            matches = re.match(pattern, host) 

            if matches:
                request.subdomain = matches.group('subdomain')
            else:
                request.subdomain = None
                logger.warning('The host %s does not belong to the domain %s, '
                    'unable to identify the subdomain for this request',
                    request.get_host())


class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    """
    A middleware class that allows for subdomain-based URL routing.
    """
    def process_request(self, request):
        """
        Sets the current request's ``urlconf`` attribute to the urlconf
        associated with the subdomain, if it is listed in
        ``settings.SUBDOMAIN_URLCONFS``.
        """
        super(SubdomainURLRoutingMiddleware, self).process_request(request)

        subdomain = getattr(request, 'subdomain', UNSET)

        if subdomain is not UNSET:
            urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain)
            if urlconf is not None:
                logger.debug("Using urlconf %s for subdomain: %s",
                    repr(urlconf), repr(subdomain))
                request.urlconf = urlconf

    def process_response(self, request, response):
        """
        Forces the HTTP ``Vary`` header onto requests to avoid having responses
        cached across subdomains.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))

        return response

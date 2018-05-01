django-subdomains
=================

Subdomain helpers for the Django framework, including subdomain-based URL
routing and reversing.

Full documentation can be found here: http://django-subdomains.readthedocs.org/

Amboss Customization
--------------------

Drop the SITE framework dependency and instead simplify the subdomain 
extraction: just take the first part of the domain string and use that for the
subdomain.

Build Status
------------

.. image:: https://secure.travis-ci.org/tkaemming/django-subdomains.png?branch=master
   :target: http://travis-ci.org/tkaemming/django-subdomains

Tested on Python 2.6, 2.7, 3.4 and 3.5 on their supported Django versions from
1.4 through 1.9.

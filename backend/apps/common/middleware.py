# -*- coding: utf-8 -*-
"""
Middewares comunes
==================
"""

import re

from django.http import HttpResponseRedirect


class IEDetectionMiddleware(object):
    """
    Middleware para detectar versiones anteriores de Internet Explorer y
    redireccionar al usuario hacia browsehappy.com.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            pattern = 'msie [1-8]\.'
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)
            if match:
                return HttpResponseRedirect('http://browsehappy.com/?locale=es')
        response = self.get_response(request)
        return response

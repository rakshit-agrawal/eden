# -*- coding: utf-8 -*-

"""
    QuickResponseHost Module - Controllers
"""

__author__ = 'rakshit'

module = request.controller

if not settings.has_module(module):
    raise HTTP(404, body="Module disabled: %s" % module)


# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    # Page title
    module_name = settings.modules[module].name_nice

    response.title = module_name
    output = {"module_name": module_name}

    return output

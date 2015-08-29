# -*- coding: utf-8 -*-

"""
    QuickResponseHost Module - Controllers
"""

__author__ = 'rakshit'

module = request.controller

if not settings.has_module(module):
    raise HTTP(404, body="Module disabled: %s" % module)


def host_volunteer(function = None, results={}):
    if function == "base":
        results['name'] = "Volunteer"
    elif function == "create":
        results['name'] = "Create a new volunteer"
    elif function == "list":
        results['name'] = "List all volunteers"
    return results


def host_assets(function = None, results={}):
    if function == "base":
        results['name'] = "Assets"
    elif function == "create":
        results['name'] = "Create an asset"
    elif function == "list":
        results['name'] = "List all assets"
    return results


HOSTS = {
    'volunteer': host_volunteer,
    'assets': host_assets,
}


# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    # Page title
    module_name = settings.modules[module].name_nice

    response.title = module_name
    output = {"module_name": module_name}

    return output


def base():
    """
    Base page for the kind of QRH being used.
    Type of module to use will be identified through first argument
    :return:
    """
    if len(request.args)>0:
        host_type = request.args(0)
    else:
        redirect(URL('qrh','index'))

    try:
        return_fields = HOSTS[host_type](function="base")
    except KeyError, e:
        redirect(URL('qrh','index'))


    return return_fields


def create_entry():
    """
    Base page for the kind of QRH being used.
    Type of module to use will be identified through first argument
    :return:
    """
    if len(request.args)>0:
        host_type = request.args(0)
    else:
        redirect(URL('qrh','index'))

    try:
        return_fields = HOSTS[host_type](function="create")
    except KeyError, e:
        redirect(URL('qrh','index'))

    return return_fields

def list_entries():
    """
    Base page for the kind of QRH being used.
    Type of module to use will be identified through first argument
    :return:
    """
    if len(request.args)>0:
        host_type = request.args(0)
    else:
        redirect(URL('qrh','index'))

    try:
        return_fields = HOSTS[host_type](function="list")
    except KeyError, e:
        redirect(URL('qrh','index'))

    return return_fields

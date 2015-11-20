# -*- coding: utf-8 -*-

"""
    QuickResponseHost Module - Controllers
"""
from s3.s3forms import S3SQLCustomForm, S3SQLInlineComponent


__author__ = 'rakshit'

module = request.controller

if not settings.has_module(module):
    raise HTTP(404, body="Module disabled: %s" % module)

def nothing(function=None, results={}):
    if function == "base":
        results['name'] = "QuickResponseHost"
        results['message'] = "Please select the host type"
        results['options'] = []
        for i in [key for key in HOSTS.keys() if key!="nothing"]:
            results['options'].append(dict(object = A(i.title(),
                                                      target=URL('qrh','base',args=[i]),
                                                      _class='btn btn-default btn-block btn-lg main-btn col-md-6',
                                                      _role='button',
                                                      _href=URL('qrh','base',args=[i])),
                                           action="base"))

        return results


def host_volunteer(function = None, results={}, category=None):
    if function == "base":
        results['name'] = "Volunteer"
        results['message'] = "I would like to"
        results['options'] = []
        results['options'].append(dict(object = A('Register a new volunteer',
                                                  target=URL('qrh','create_entry',args=["volunteer"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','create_entry',args=["volunteer"])),
                                       action="create"))
        results['options'].append(dict(object = A('View current volunteers',
                                                  target=URL('qrh','list_entries',args=["volunteer"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','list_entries',args=["volunteer"])),
                                       action="list"))

    elif function == "create":
        results['name'] = "Create a new volunteer"
        results['message'] = "The new volunteer is a.."
        results['options'] = []
        results['options'].append(dict(object = A('Volunteer with first aid skills',
                                                  target=URL('qrh','entry',args=["volunteer", "first_aid"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','entry',args=["volunteer", "first_aid"])),
                                       action="create"))
        results['options'].append(dict(object = A('Volunteer with tech support skills',
                                                  target=URL('qrh','entry',args=["volunteer", "tech_support"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','entry',args=["volunteer", "tech_support"])),
                                       action="create"))
        results['options'].append(dict(object = A('Lead volunteer',
                                                  target=URL('qrh','entry',args=["volunteer", "lead"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','entry',args=["volunteer", "lead"])),
                                       action="create"))
        results['options'].append(dict(object = A('General volunteer',
                                                  target=URL('qrh','entry',args=["volunteer", "general"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','entry',args=["volunteer", "general"])),
                                       action="create"))

    elif function == "entry":
        # Perform preset functions of Tech Support entry
        """
            Name
            Dat of Birth
            Sex
            Normal job
            Mobile Phone
            Email
            Organization
            Past job records
        """
        #form = SQLFORM.factory(s3db.hrm_human_resource, s3db.pr_person_details)
        form = SQLFORM(s3db.qrhvolunteer)
        print category
        form.vars.role = (category.replace('_', ' ')).title() if not None else ""
        print form

        if form.process().accepted:
            redirect(URL('qrh','base'))

        results['message'] = "Volunteer details are:"
        results['form'] = form
        results['to_hide'] = ['#qrhvolunteer_dob__row', '#qrhvolunteer_role__row']

    elif function == "list":
        results['name'] = "List all volunteers"


    return results


def host_assets(function = None, results={}):
    if function == "base":
        results['name'] = "Assets"
        results['message'] = "I would like to"
        results['options'] = []
        results['options'].append(dict(object = A('Register a new asset',
                                                  target=URL('qrh','create_entry',args=["assets"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','create_entry',args=["assets"])),
                                       action="create"))
        results['options'].append(dict(object = A('View current assets',
                                                  target=URL('qrh','list_entries',args=["assets"]),
                                                  _class='btn btn-default btn-block btn-lg main-btn',
                                                  _role='button',
                                                  _href=URL('qrh','list_entries',args=["assets"])),
                                       action="list"))

    elif function == "create":
        results['name'] = "Create an asset"
        results['message'] = "The new asset is.. "
        results['options'] = []


    elif function == "list":
        results['name'] = "List all assets"
    return results


HOSTS = {
    'nothing': nothing,
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
    redirect(URL('qrh','base'))
    return output

def qrhheader():
    return dict(module_list=HOSTS.keys())

def base():
    """
    Base page for the kind of QRH being used.
    Type of module to use will be identified through first argument
    :return:
    """
    if len(request.args)>0:
        host_type = request.args(0)
    else:
        host_type = "nothing"

    try:
        return_fields = HOSTS[host_type](function="base")
    except KeyError, e:
        redirect(URL('qrh','index'))

    return_fields['host_type'] = host_type.title()
    return_fields['module_list'] = [key.title() for key in HOSTS.keys() if key!="nothing"]

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

    if len(request.args)==1:
        try:
            return_fields = HOSTS[host_type](function="create")
        except KeyError, e:
            redirect(URL('qrh','index'))
    elif len(request.args)==2 and request.args(1)=="specialized":
        # Then perform specialized category tasks
        if request.vars.has_key('category'):
            # Perform actions as per the category
            try:
                category = request.vars['category']
                return_fields = HOSTS[host_type](function="create", category=category)
            except KeyError, e:
                redirect(URL('qrh','index'))

                pass


    return_fields['host_type'] = host_type.title()
    return_fields['module_list'] = [key.title() for key in HOSTS.keys() if key!="nothing"]

    return return_fields

def entry():
    """

    :return:
    """
    if len(request.args)>0:
        host_type = request.args(0)
    else:
        redirect(URL('qrh','index'))

    if len(request.args)>1:
        try:
            category = request.args(1)

            return_fields = HOSTS[host_type](function="entry", category=category)
        except KeyError, e:
            redirect(URL('qrh','index'))

    else:
            return_fields = HOSTS[host_type](function="entry")


    return_fields['host_type'] = host_type.title()
    return_fields['module_list'] = [key.title() for key in HOSTS.keys() if key!="nothing"]

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

    return_fields['host_type'] = host_type.title()
    return_fields['module_list'] = [key.title() for key in HOSTS.keys() if key!="nothing"]

    return return_fields

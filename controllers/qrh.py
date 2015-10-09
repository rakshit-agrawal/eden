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
        form = SQLFORM.factory(
            Field('name',label="Name"),
            Field('dob', 'date',label = "Date of Birth"),
            Field('sex',requires=IS_IN_SET(("Male", "Female", "Other")), widget = SQLFORM.widgets.radio.widget),
            Field('mobile', label="Mobile No."),
            Field('email', label="Email", requires = IS_EMAIL(error_message='invalid email!')),
            Field('role', readable = (category is None),writable = (category is None))
        )



        # Volunteers only
        s3.filter = FS("type") == 2

        vol_experience = settings.get_hrm_vol_experience()

        def prep(r):
            resource = r.resource
            get_config = resource.get_config

            # CRUD String
            s3.crud_strings[resource.tablename] = s3.crud_strings["hrm_volunteer"]

            # Default to volunteers
            table = r.table
            table.type.default = 2

            # Volunteers use home address
            location_id = table.location_id
            location_id.label = T("Home Address")

            # Configure list_fields
            if r.representation == "xls":
                # Split person_id into first/middle/last to
                # make it match Import sheets
                list_fields = ["person_id$first_name",
                               "person_id$middle_name",
                               "person_id$last_name",
                               ]
            else:
                list_fields = ["person_id",
                               ]
            list_fields.append("job_title_id")
            if settings.get_hrm_multiple_orgs():
                list_fields.append("organisation_id")
            list_fields.extend(((settings.get_ui_label_mobile_phone(), "phone.value"),
                                (T("Email"), "email.value"),
                                "location_id",
                                ))
            if settings.get_hrm_use_trainings():
                list_fields.append((T("Trainings"),"person_id$training.course_id"))
            if settings.get_hrm_use_certificates():
                list_fields.append((T("Certificates"),"person_id$certification.certificate_id"))

            # Volunteer Programme and Active-status
            report_options = get_config("report_options")
            if vol_experience in ("programme", "both"):
                # Don't use status field
                table.status.readable = table.status.writable = False
                # Use active field?
                vol_active = settings.get_hrm_vol_active()
                if vol_active:
                    list_fields.insert(3, (T("Active?"), "details.active"))
                # Add Programme to List Fields
                list_fields.insert(6, "person_id$hours.programme_id")

                # Add active and programme to Report Options
                report_fields = report_options.rows
                report_fields.append("person_id$hours.programme_id")
                if vol_active:
                    report_fields.append((T("Active?"), "details.active"))
                report_options.rows = report_fields
                report_options.cols = report_fields
                report_options.fact = report_fields
            else:
                # Use status field
                list_fields.append("status")

            # Update filter widgets
            filter_widgets = \
                s3db.hrm_human_resource_filters(resource_type="volunteer",
                                                hrm_type_opts=s3db.hrm_type_opts)

            # Reconfigure
            resource.configure(list_fields = list_fields,
                               filter_widgets = filter_widgets,
                               report_options = report_options,
                               )

            if r.interactive:
                if r.id:
                    if r.method not in ("profile", "delete"):
                        # Redirect to person controller
                        vars = {"human_resource.id": r.id,
                                "group": "volunteer"
                                }
                        if r.representation == "iframe":
                            vars["format"] = "iframe"
                            args = [r.method]
                        else:
                            args = []
                        redirect(URL('volunteerCategories/'))
                else:
                    if r.method == "import":
                        # Redirect to person controller
                        redirect(URL(f="person",
                                     args="import",
                                     vars={"group": "volunteer"}))

                    elif not r.component and r.method != "delete":
                        # Configure AddPersonWidget
                        table.person_id.widget = S3AddPersonWidget2(controller="vol")
                        # Show location ID
                        location_id.writable = location_id.readable = True
                        # Hide unwanted fields
                        for fn in ("site_id",
                                   "code",
                                   "department_id",
                                   "essential",
                                   "site_contact",
                                   "status",
                                   ):
                            table[fn].writable = table[fn].readable = False
                        # Organisation Dependent Fields
                        set_org_dependent_field = settings.set_org_dependent_field
                        set_org_dependent_field("pr_person_details", "father_name")
                        set_org_dependent_field("pr_person_details", "mother_name")
                        set_org_dependent_field("pr_person_details", "affiliations")
                        set_org_dependent_field("pr_person_details", "company")
                        set_org_dependent_field("vol_details", "availability")
                        set_org_dependent_field("vol_volunteer_cluster", "vol_cluster_type_id")
                        set_org_dependent_field("vol_volunteer_cluster", "vol_cluster_id")
                        set_org_dependent_field("vol_volunteer_cluster", "vol_cluster_position_id")
                        # Label for "occupation"
                        s3db.pr_person_details.occupation.label = T("Normal Job")
                        # Assume volunteers only between 12-81
                        s3db.pr_person.date_of_birth.widget = S3DateWidget(past=972, future=-144)
            return True
        s3.prep = prep

        def postp(r, output):
            if r.interactive and not r.component:
                # Set the minimum end_date to the same as the start_date
                s3.jquery_ready.append(
    '''S3.start_end_date('hrm_human_resource_start_date','hrm_human_resource_end_date')''')

                # Configure action buttons
                s3_action_buttons(r, deletable=settings.get_hrm_deletable())
                if "msg" in settings.modules and \
                   settings.get_hrm_compose_button() and \
                   auth.permission.has_permission("update", c="hrm", f="compose"):
                    # @ToDo: Remove this now that we have it in Events?
                    s3.actions.append({
                            "url": URL(f="compose",
                                        vars = {"human_resource.id": "[id]"}),
                            "_class": "action-btn send",
                            "label": str(T("Send Message"))
                        })

                # Insert field to set the Programme
                if vol_experience in ("programme", "both") and \
                   r.method not in ("search", "report", "import") and \
                   "form" in output:
                    # @ToDo: Re-implement using
                    # http://eden.sahanafoundation.org/wiki/S3SQLForm
                    # NB This means adjusting IFRC/config.py too
                    sep = ": "
                    table = s3db.hrm_programme_hours
                    field = table.programme_id
                    default = field.default
                    widget = field.widget or SQLFORM.widgets.options.widget(field, default)
                    field_id = "%s_%s" % (table._tablename, field.name)
                    label = field.label
                    row_id = field_id + SQLFORM.ID_ROW_SUFFIX
                    if s3_formstyle == "bootstrap":
                        label = LABEL(label, label and sep, _class="control-label", _for=field_id)
                        _controls = DIV(widget, _class="controls")
                        row = DIV(label, _controls,
                                    _class="control-group",
                                    _id=row_id,
                                    )
                        output["form"][0].insert(4, row)
                    elif callable(s3_formstyle):
                        label = LABEL(label, label and sep, _for=field_id,
                                        _id=field_id + SQLFORM.ID_LABEL_SUFFIX)
                        programme = s3_formstyle(row_id, label, widget,
                                                    field.comment)
                        if isinstance(programme, DIV) and \
                           "form-row" in programme["_class"]:
                            # Foundation formstyle
                            output["form"][0].insert(4, programme)
                        else:
                            try:
                                output["form"][0].insert(4, programme[1])
                            except:
                                # A non-standard formstyle with just a single row
                                pass
                            try:
                                output["form"][0].insert(4, programme[0])
                            except:
                                pass
                    else:
                        # Unsupported
                        raise

            elif r.representation == "plain":
                # Map Popups
                output = s3db.hrm_map_popup(r)
            return output
        s3.postp = postp

        controller =  s3_rest_controller("hrm", "human_resource",
                                         create_next='/eden/qrh/entry',
                                         update_next='/eden/qrh/entry')
        response.view = "qrh/entry.html"
        form = controller['form']
        form.vars.organisation_id = 1
        form.vars.job_title_id = "test"

        exclude_fields = [
                'no_table_pe_label__row',
                'hrm_human_resource_organisation_id__row',
                'no_table_site_id__row',
                'no_table_code__row',
                'hrm_human_resource_job_title_id__row',
                'no_table_department_id__row',
                'no_table_essential__row',
                'hrm_human_resource_start_date__row',
                'no_table_status__row',
                'no_table_preferred_name__row',
                'no_table_initials__row',
                'no_table_local_name__row',
                'no_table_site_contact__row']
        leadText = ''

        for row in form.components[0].elements('div'):
            if row['_id'] in exclude_fields:
                row['_class'] = ' collapse'
            #if row['attributes']['_id'] in exclude_fields:
                #row['_class'] = 'collapse'
        showFields = DIV(A(SPAN('Show/Hide All Fields', _class="filter-advanced-label"), _class="filter-advanced", _id="showFields"), _class="filter-controls")
        form[0].insert(-1,showFields)
        if form.process().accepted:
            pass
        elif form.errors:
            pass



        #if form.validate():

        #    if category == "first_aid":
        #        role = "First Aid"
        #        redirect(URL('qrh',form.vars.name))

        results['message'] = "Volunteer details are:"
        results['form'] = form

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

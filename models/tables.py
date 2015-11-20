from datetime import datetime
s3db.define_table('qrhvolunteer',
                  Field('name', label="Name", requires=IS_NOT_EMPTY(error_message='Please provide a name'),),
                  Field('sex', requires=IS_IN_SET(("Male", "Female", "Do not wish to disclose")), widget=SQLFORM.widgets.radio.widget),
                  Field('mobile', label="Mobile No."),
                  Field('email', label="Email", requires=IS_EMAIL(error_message='Invalid email!')),
                  Field('role', ),
                  Field('dob', 'date', label="Date of Birth"),
                  Field('organization',),
                  Field('normal_job'),
                  Field('doj','datetime',default=datetime.utcnow(), readable=False, writable=False)
                  )

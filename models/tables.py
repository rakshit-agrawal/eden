
s3db.define_table('qrhvolunteer',
            Field('name',label="Name"),
            Field('sex',requires=IS_IN_SET(("Male", "Female", "Other")), widget = SQLFORM.widgets.radio.widget),
            Field('mobile', label="Mobile No."),
            Field('email', label="Email", requires = IS_EMAIL(error_message='invalid email!')),
            Field('role',),
            Field('dob', 'date',label = "Date of Birth"),

        )
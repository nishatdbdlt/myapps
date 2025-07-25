# -*- coding: utf-8 -*-
{
    'name': "students",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
          'views/views.xml',
        'views/templates.xml',
        'views/report.xml',
        'views/class.xml',
        'views/student.xml',
        'views/shift.xml',
        'views/section.xml',
        'views/student_wizard_report.xml',
        'views/blood.xml',
        'views/hide.xml',
        'views/blood_group.xml',
        'views/class_report.xml',
        'views/teacher.xml',
        'views/subject.xml',
        'views/class_report.xml',
        'views/class_teacher.xml',
        'views/student_id_template.xml',
        'views/student_id.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


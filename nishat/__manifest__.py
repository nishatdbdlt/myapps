# -*- coding: utf-8 -*-
{
    'name': "nishat",

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
    'depends': ['base','library','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/book.xml',
        'views/issued.xml',
        'views/report.xml',
        'views/active_member.xml',

         'views/views.xml',
        'views/templates.xml',
        'views/library.xml',
        'views/issue.xml',
        'views/library_user.xml',
        'views/product_tag.xml',
        'views/product_temp.xml',
        'views/member.xml',
        'views/edu_active.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


# -*- coding: utf-8 -*-
{
    'name': "garments_management",

    'summary': "Short",

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
    'depends': ['base','product'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/sequence.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/garments_order.xml',
        'views/inventory.xml',
        'views/garments_production.xml',
        'views/inventory.xml',
        'views/parchase_line.xml',
        'views/perchuse.xml',
        'views/product.xml',
        'views/garments_perchase.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


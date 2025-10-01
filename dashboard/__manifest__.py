# -*- coding: utf-8 -*-
{
    'name': "dashboard",
    'summary': "Custom KPI Dashboard",
    'description': """
Interactive dashboard for Sales KPI using OWL and Odoo 17
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': [
        'base',
        'crm',
        'web',
        'sale',
        'sale_management','board','mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/kpi.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard/static/src/js/dashboard.js',
            'dashboard/static/src/xml/dashboard_template.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

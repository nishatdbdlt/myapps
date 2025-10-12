# -*- coding: utf-8 -*-
# from odoo import http


# class PreSalesManagement(http.Controller):
#     @http.route('/pre_sales_management/pre_sales_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pre_sales_management/pre_sales_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pre_sales_management.listing', {
#             'root': '/pre_sales_management/pre_sales_management',
#             'objects': http.request.env['pre_sales_management.pre_sales_management'].search([]),
#         })

#     @http.route('/pre_sales_management/pre_sales_management/objects/<model("pre_sales_management.pre_sales_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pre_sales_management.object', {
#             'object': obj
#         })


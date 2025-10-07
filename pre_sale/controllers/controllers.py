# -*- coding: utf-8 -*-
# from odoo import http


# class PreSale(http.Controller):
#     @http.route('/pre_sale/pre_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pre_sale/pre_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pre_sale.listing', {
#             'root': '/pre_sale/pre_sale',
#             'objects': http.request.env['pre_sale.pre_sale'].search([]),
#         })

#     @http.route('/pre_sale/pre_sale/objects/<model("pre_sale.pre_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pre_sale.object', {
#             'object': obj
#         })


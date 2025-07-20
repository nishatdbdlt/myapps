# -*- coding: utf-8 -*-
# from odoo import http


# class Inventory2(http.Controller):
#     @http.route('/inventory2/inventory2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory2/inventory2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory2.listing', {
#             'root': '/inventory2/inventory2',
#             'objects': http.request.env['inventory2.inventory2'].search([]),
#         })

#     @http.route('/inventory2/inventory2/objects/<model("inventory2.inventory2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory2.object', {
#             'object': obj
#         })


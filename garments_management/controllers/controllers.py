# -*- coding: utf-8 -*-
# from odoo import http


# class GarmentsManagement(http.Controller):
#     @http.route('/garments_management/garments_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/garments_management/garments_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('garments_management.listing', {
#             'root': '/garments_management/garments_management',
#             'objects': http.request.env['garments_management.garments_management'].search([]),
#         })

#     @http.route('/garments_management/garments_management/objects/<model("garments_management.garments_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('garments_management.object', {
#             'object': obj
#         })


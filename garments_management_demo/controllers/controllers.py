# -*- coding: utf-8 -*-
# from odoo import http


# class GarmentsManagementDemo(http.Controller):
#     @http.route('/garments_management_demo/garments_management_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/garments_management_demo/garments_management_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('garments_management_demo.listing', {
#             'root': '/garments_management_demo/garments_management_demo',
#             'objects': http.request.env['garments_management_demo.garments_management_demo'].search([]),
#         })

#     @http.route('/garments_management_demo/garments_management_demo/objects/<model("garments_management_demo.garments_management_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('garments_management_demo.object', {
#             'object': obj
#         })


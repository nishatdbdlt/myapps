# -*- coding: utf-8 -*-
# from odoo import http


# class Bangladesh(http.Controller):
#     @http.route('/bangladesh/bangladesh', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bangladesh/bangladesh/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bangladesh.listing', {
#             'root': '/bangladesh/bangladesh',
#             'objects': http.request.env['bangladesh.bangladesh'].search([]),
#         })

#     @http.route('/bangladesh/bangladesh/objects/<model("bangladesh.bangladesh"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bangladesh.object', {
#             'object': obj
#         })


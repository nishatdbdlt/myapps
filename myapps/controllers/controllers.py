# -*- coding: utf-8 -*-
# from odoo import http


# class Myapps(http.Controller):
#     @http.route('/myapps/myapps', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/myapps/myapps/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('myapps.listing', {
#             'root': '/myapps/myapps',
#             'objects': http.request.env['myapps.myapps'].search([]),
#         })

#     @http.route('/myapps/myapps/objects/<model("myapps.myapps"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('myapps.object', {
#             'object': obj
#         })


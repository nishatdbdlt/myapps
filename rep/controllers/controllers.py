# -*- coding: utf-8 -*-
# from odoo import http


# class Rep(http.Controller):
#     @http.route('/rep/rep', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rep/rep/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rep.listing', {
#             'root': '/rep/rep',
#             'objects': http.request.env['rep.rep'].search([]),
#         })

#     @http.route('/rep/rep/objects/<model("rep.rep"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rep.object', {
#             'object': obj
#         })


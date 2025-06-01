# -*- coding: utf-8 -*-
# from odoo import http


# class Nishat(http.Controller):
#     @http.route('/nishat/nishat', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nishat/nishat/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nishat.listing', {
#             'root': '/nishat/nishat',
#             'objects': http.request.env['nishat.nishat'].search([]),
#         })

#     @http.route('/nishat/nishat/objects/<model("nishat.nishat"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nishat.object', {
#             'object': obj
#         })


# -*- coding: utf-8 -*-
# from odoo import http


# class Stock(http.Controller):
#     @http.route('/stock/stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock/stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock.listing', {
#             'root': '/stock/stock',
#             'objects': http.request.env['stock.stock'].search([]),
#         })

#     @http.route('/stock/stock/objects/<model("stock.stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock.object', {
#             'object': obj
#         })


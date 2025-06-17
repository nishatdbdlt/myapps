# manage_retail_erp/models/sales.py

from odoo import models, fields, api

class RetailSales(models.Model):
    _name = 'retail.sales'
    _description = 'Retail Sales Management'

    name = fields.Char(string='Sales Reference', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('retail.sales'))

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_name = fields.Char( string='product', required=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    price_unit = fields.Float(string='Unit Price', required=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total', store=True)
    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('due', 'Due'),
        ('partial', 'Partial'),
    ], string='Payment Status', default='due')
    sale_date = fields.Date(string='Sale Date', default=fields.Date.today)

    @api.depends('quantity', 'price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.price_unit

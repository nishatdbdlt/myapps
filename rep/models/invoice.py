# manage_retail_erp/models/invoice.py

from odoo import models, fields, api

class RetailInvoice(models.Model):
    _name = 'retail.invoice'
    _description = 'Retail Invoice'

    name = fields.Char(string='Invoice Number', required=True, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('retail.invoice'))
    sale_id = fields.Many2one('retail.sales', string='Related Sale', required=True)
    customer_id = fields.Many2one(related='sale_id.customer_id', string='Customer', store=True)
    total_amount = fields.Float(related='sale_id.total_price', string='Amount', store=True)
    payment_status = fields.Selection(related='sale_id.payment_status', string='Payment Status', store=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today)

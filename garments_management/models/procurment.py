from odoo import models, fields, api

class GarmentInvoice(models.Model):
    _name = 'garment.invoice'
    _description = 'Invoice (বিল)'
    _inherit = ['mail.thread']

    name = fields.Char('ইনভয়েস নং', default=lambda self: self.env['ir.sequence'].next_by_code('garment.invoice'))
    date = fields.Date('তারিখ', default=fields.Date.today())
    customer_id = fields.Many2one('res.partner', 'গ্রাহক', required=True)
    delivery_id = fields.Many2one('garment.delivery', 'চালান রেফারেন্স')
    line_ids = fields.One2many('garment.invoice.line', 'invoice_id', 'আইটেমসমূহ')
    amount_total = fields.Float('মোট Amount', compute='_compute_total')
    state = fields.Selection([
        ('draft', 'খসড়া'),
        ('paid', 'পরিশোধিত')],
        default='draft', string='স্ট্যাটাস')

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.amount_total = sum(line.subtotal for line in rec.line_ids)

class InvoiceLine(models.Model):
    _name = 'garment.invoice.line'
    _description = 'Invoice Line Items'

    product_id = fields.Many2one('garment.product', 'পণ্য', required=True)
    quantity = fields.Float('পরিমাণ', required=True)
    price_unit = fields.Float('দর', required=True)
    subtotal = fields.Float('সাবটোটাল', compute='_compute_subtotal')
    invoice_id = fields.Many2one('garment.invoice', 'ইনভয়েস')

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
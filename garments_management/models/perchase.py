from odoo import models, fields, api
from odoo.exceptions import UserError

class GarmentPurchase(models.Model):
    _name = 'garment.purchase'
    _description = 'Garment Purchase Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'order_date desc'

    name = fields.Char(
        string='PO Number',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('garment.purchase')
    )

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        required=True,
        domain="[('is_company', '=', True)]"
    )

    order_date = fields.Date(
        string='Order Date',
        default=fields.Date.context_today,
        required=True
    )
    eta = fields.Date(
        string='Expected Delivery Date',
        help="Expected arrival date of the goods"
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('received', 'Received'),
            ('canceled', 'Canceled')
        ],
        string='Status',
        default='draft',
        tracking=True
    )

    line_ids = fields.One2many(
        'garment.purchase.line',
        'order_id',
        string='Order Lines',
        copy=True
    )

    notes = fields.Text('Terms and Conditions')

    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_total_qty',
        store=True
    )
    received_percentage = fields.Float(
        string='Received %',
        compute='_compute_received_percentage',
        store=True
    )

    @api.depends('line_ids.quantity')
    def _compute_total_qty(self):
        for order in self:
            order.total_qty = sum(line.quantity for line in order.line_ids)

    @api.depends('line_ids.quantity', 'line_ids.received_qty')
    def _compute_received_percentage(self):
        for order in self:
            total = sum(line.quantity for line in order.line_ids)
            received = sum(line.received_qty for line in order.line_ids)
            order.received_percentage = (received / total) * 100 if total else 0

    def action_confirm(self):
        for order in self:
            if not order.line_ids:
                raise UserError("You cannot confirm a purchase order without any order lines.")
            order.state = 'confirmed'

    def action_receive(self):
        for order in self:
            order.state = 'received'

    def action_reset_draft(self):
        for order in self:
            order.state = 'draft'

    def action_cancel(self):
        for order in self:
            order.state = 'canceled'

    def unlink(self):
        for order in self:
            if order.state not in ('draft', 'canceled'):
                raise UserError("You can only delete draft or canceled purchase orders.")
        return super(GarmentPurchase, self).unlink()


class GarmentPurchaseLine(models.Model):
    _name = 'garment.purchase.line'
    _description = 'Garment Purchase Order Line'
    _rec_name = 'product_id'

    order_id = fields.Many2one(
        'garment.purchase',
        string='Purchase Order',
        required=True,
        ondelete='cascade',
        index=True
    )

    # garment.product model এ যুক্ত করো
    standard_price = fields.Float(
        string='Cost Price',
        digits=(12, 2)
    )

    product_id = fields.Many2one(
        'garment.product',
        string='Product',
        required=True,
        domain="[('product_type', 'in', ['raw', 'accessory'])]"
    )

    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
        digits=(12, 4)
    )

    received_qty = fields.Float(
        string='Received Quantity',
        default=0.0,
        digits=(12, 4)
    )

    price_unit = fields.Float(
        string='Unit Price',
        digits=(12, 2)
    )

    subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        currency_field='currency_id'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        readonly=True,
        store=True
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.standard_price or 0.0

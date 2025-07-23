from odoo import models, fields
from odoo.exceptions import UserError
from odoo import fields as odoo_fields

class PurchaseOrder(models.Model):
    _name = 'smartstock.purchase.order'
    _description = 'Purchase Order'

    name = fields.Char(string="PO Reference", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('smartstock.purchase.order'))
    vendor_id = fields.Many2one('smartstock.vendor', string="Vendor", required=True)
    order_date = fields.Date(string="Order Date", default=odoo_fields.Date.today)
    order_line_ids = fields.One2many('smartstock.purchase.order.line', 'order_id', string="Order Lines")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received')
    ], default='draft')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_receive(self):
        for line in self.order_line_ids:
            self.env['smartstock.stock.movement'].create({
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'source_location_id': False,
                'dest_location_id': line.destination_location_id.id,
                'movement_date': fields.Datetime.now(),
                'note': f'Purchase Receipt for PO {self.name}',
            })
        self.state = 'received'


class PurchaseOrderLine(models.Model):
    _name = 'smartstock.purchase.order.line'
    _description = 'Purchase Order Line'

    order_id = fields.Many2one('smartstock.purchase.order', string="Purchase Order", required=True, ondelete='cascade')
    product_id = fields.Many2one('smartstock.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    price_unit = fields.Float(string="Unit Price")
    destination_location_id = fields.Many2one('smartstock.stock.location', string="Destination Location")

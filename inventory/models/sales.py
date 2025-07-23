from odoo import models, fields
from odoo.exceptions import UserError
from odoo import fields as odoo_fields

class SaleOrder(models.Model):
    _name = 'smartstock.sale.order'
    _description = 'Sale Order'

    name = fields.Char(string="SO Reference", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('smartstock.sale.order'))
    customer_id = fields.Many2one('smartstock.customer', string="Customer", required=True)
    order_date = fields.Date(string="Order Date", default=odoo_fields.Date.today)
    order_line_ids = fields.One2many('smartstock.sale.order.line', 'order_id', string="Order Lines")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered')
    ], default='draft')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_deliver(self):
        for line in self.order_line_ids:
            product = line.product_id
            qty = line.quantity
            if product.quantity_on_hand < qty:
                raise UserError(f'Not enough stock for product {product.name}')
            self.env['smartstock.stock.movement'].create({
                'product_id': product.id,
                'quantity': qty,
                'source_location_id': line.source_location_id.id,
                'dest_location_id': False,
                'movement_date': fields.Datetime.now(),
                'note': f'Delivery for SO {self.name}',
            })
        self.state = 'delivered'


class SaleOrderLine(models.Model):
    _name = 'smartstock.sale.order.line'
    _description = 'Sale Order Line'

    order_id = fields.Many2one('smartstock.sale.order', string="Sale Order", required=True, ondelete='cascade')
    product_id = fields.Many2one('smartstock.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    price_unit = fields.Float(string="Unit Price")
    source_location_id = fields.Many2one('smartstock.stock.location', string="Source Location")

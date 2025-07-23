from odoo import models, fields, api
from odoo.exceptions import UserError

class StockLocation(models.Model):
    _name = 'smartstock.stock.location'
    _description = 'Stock Location'

    name = fields.Char(string="Location Name", required=True)
    parent_id = fields.Many2one('smartstock.stock.location', string="Parent Location")
    child_ids = fields.One2many('smartstock.stock.location', 'parent_id', string="Child Locations")


class StockMovement(models.Model):
    _name = 'smartstock.stock.movement'
    _description = 'Stock Movement'

    product_id = fields.Many2one('smartstock.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    source_location_id = fields.Many2one('smartstock.stock.location', string="Source Location")
    dest_location_id = fields.Many2one('smartstock.stock.location', string="Destination Location")
    movement_date = fields.Datetime(string="Movement Date", default=fields.Datetime.now)
    note = fields.Text(string="Note")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        product = self.env['smartstock.product'].browse(vals['product_id'])
        qty = vals['quantity']
        source = vals.get('source_location_id')
        dest = vals.get('dest_location_id')

        if source:
            if product.quantity_on_hand < qty:
                raise UserError(f'Not enough stock for product {product.name} in source location.')
            product.quantity_on_hand -= qty
        if dest:
            product.quantity_on_hand += qty

        product.flush()
        return record

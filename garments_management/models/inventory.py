from odoo import models, fields, api

class InventoryMovement(models.Model):
    _name = 'garment.inventory'
    _description = 'Inventory Movement'

    product_id = fields.Many2one('garment.product', 'Product', required=True)
    quantity = fields.Float('Quantity', required=True)
    movement_type = fields.Selection([
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer')], 'Type', required=True)
    source_location = fields.Char('From Location')
    destination_location = fields.Char('To Location')
    barcode_scan = fields.Char('Scan Barcode')

    @api.onchange('barcode_scan')
    def _onchange_barcode_scan(self):
        if self.barcode_scan:
            product = self.env['garment.product'].search([('barcode', '=', self.barcode_scan)], limit=1)
            if product:
                self.product_id = product
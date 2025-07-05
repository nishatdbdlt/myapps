# garment_management/models/product.py
from odoo import models, fields

class GarmentProductCategory(models.Model):
    _name = 'garment.product.category'
    _description = 'Garment Product Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')


class GarmentProduct(models.Model):
    _name = 'garment.product'
    _description = 'Garment Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Product Name', required=True, tracking=True)
    category_id = fields.Many2one('garment.product.category', string='Category', tracking=True)
    color = fields.Char(string='Color')
    size = fields.Char(string='Size')
    quantity_available = fields.Float(string='Available Qty', default=0.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price = fields.Float(string='Unit Price')
    active = fields.Boolean(default=True)

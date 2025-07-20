from odoo import models, fields

class ProductCategory(models.Model):
    _name = 'smartstock.product.category'
    _description = 'Product Category'

    name = fields.Char(string="Category Name", required=True)
    product_ids = fields.One2many('smartstock.product', 'category_id', string='Products')







from odoo import models, fields

class SmartProduct(models.Model):
    _name = 'smartstock.product'
    _description = 'Smart Product'

    name = fields.Char(string="Product Name", required=True)
    sku = fields.Char(string="SKU", required=True)
    category_id = fields.Many2one('product.category', string="Category")
    quantity_on_hand = fields.Float(string="Quantity On Hand", default=0.0)
    minimum_qty = fields.Float(string="Minimum Quantity", default=0.0)

from odoo import models, fields

class ProductTag(models.Model):
    _name = 'product.tag'
    _description = 'Product Tag'

    name = fields.Char(required=True, string="Tag Name")
    product_template_ids = fields.Many2many(
        'product.template',
        'product_tag_rel',
        'tag_id',
        'product_id',
        string="Products"
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tag_ids = fields.Many2many(
        'product.tag',
        'product_tag_rel',
        'product_id',
        'tag_id',
        string="Tags"
    )

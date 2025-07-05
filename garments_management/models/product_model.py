from odoo import models, fields, api

class GarmentProduct(models.Model):
    _name = 'garment.product'
    _description = 'Garment Products'

    name = fields.Char('Product Name', required=True)
    sku = fields.Char('SKU', unique=True)
    product_type = fields.Selection([
        ('raw', 'Raw Material'),
        ('accessory', 'Accessory'),
        ('finished', 'Finished Goods')], required=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('button', 'Button'),
        ('zipper', 'Zipper')], 'Material Type')
    color = fields.Char('Color')
    size = fields.Char('Size')
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    barcode = fields.Char('Barcode', copy=False, index=True)
    category = fields.Selection([
        ('knit', 'Knit'),
        ('woven', 'Woven')], 'Category')
    active = fields.Boolean('Active', default=True)
    standard_price = fields.Float(string='Standard Price')

    # স্বয়ংক্রিয় বারকোড জেনারেটর
    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('garment.barcode')
        return super().create(vals)
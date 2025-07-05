from odoo import models, fields, api

class ProductionOrder(models.Model):
    _name = 'garment.production'
    _description = 'Production Order'

    name = fields.Char(
        string='PO Number',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('garment.purchase')
    )

    product_id = fields.Many2one(
        'garment.product',
        string='Product',
        domain=[('product_type', '=', 'finished')],
        required=True
    )

    bom_id = fields.Many2one(
        'garment.bom',
        string='Bill of Materials',
        domain="[('product_id', '=', product_id)]"
    )

    quantity = fields.Float('Quantity', default=1.0)
    stage = fields.Selection([
        ('cutting', 'Cutting'),
        ('sewing', 'Sewing'),
        ('finishing', 'Finishing'),
        ('packing', 'Packing'),
    ], string='Stage', default='cutting')

    start_date = fields.Datetime('Start Time')
    end_date = fields.Datetime('End Time')
    wastage = fields.Float('Wastage %')
    team_id = fields.Many2one('garment.team', 'Production Team')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            bom = self.env['garment.bom'].search([('product_id', '=', self.product_id.id)], limit=1)
            self.bom_id = bom or False


class GarmentBOM(models.Model):
    _name = 'garment.bom'
    _description = 'Bill of Materials'

    name = fields.Char('Name', required=True)
    product_id = fields.Many2one('garment.product', 'Finished Product', required=True)
    line_ids = fields.One2many('garment.bom.line', 'bom_id', 'Components')


class BOMLine(models.Model):
    _name = 'garment.bom.line'
    _description = 'BOM Line'

    product_id = fields.Many2one('garment.product', 'Component', required=True)
    quantity = fields.Float('Quantity', default=1.0, required=True)
    bom_id = fields.Many2one('garment.bom', 'Parent BOM', required=True)

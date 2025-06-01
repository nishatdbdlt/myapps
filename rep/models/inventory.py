# manage_retail_erp/models/inventory.py

from odoo import models, fields, api

class RetailInventory(models.Model):
    _name = 'retail.inventory'
    _description = 'Retail Inventory Management'

    name = fields.Char(string='Product Name', required=True)
    product_code = fields.Char(string='Product Code')
    quantity_available = fields.Integer(string='Quantity Available', default=0)
    reorder_level = fields.Integer(string='Reorder Level', default=10)
    last_restock_date = fields.Date(string='Last Restocked On')
    is_below_reorder = fields.Boolean(string='Below Reorder Level', compute='_compute_reorder_status', store=True)

    @api.depends('quantity_available', 'reorder_level')
    def _compute_reorder_status(self):
        for rec in self:
            rec.is_below_reorder = rec.quantity_available <= rec.reorder_level

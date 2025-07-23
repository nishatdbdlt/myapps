# custom_erp/models/sale_order.py
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_deadline = fields.Date(string='Delivery Deadline')

    @api.model
    def create(self, vals):
        # অটোমেটিক নাম্বারিং: sale.order এর sequence ব্যবহার
        if not vals.get('name') or vals.get('name') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or '/'
        return super().create(vals)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.delivery_deadline:
                # TODO: Cron / Automated Action দিয়ে রিমাইন্ডার পাঠানোর লজিক
                pass
        return res

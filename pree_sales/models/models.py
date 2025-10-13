from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'res.partner'

    bidding_amount = fields.Char(string='Bidding Amount')

    client_user = fields.Char(string='Client User Name')
    user_code = fields.Char(string='User ID')
    client_name = fields.Char(string='Client Display Name')

    Sbus_id = fields.Char(string='Company Name')
    date = fields.Date(string='Date')

    Service_type = fields.Char(string='Service Type')
    bidding_status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('won', 'Won'),
        ('lost', 'Lost')
    ], string='Bidding Status', default='draft')

    payment_status = fields.Selection([
        ('sold', 'Sold'),
        ('unsold', 'Unsold'),
    ], string='Payment Status')

    client_category = fields.Selection([
        ('new', 'New'),
        ('existing', 'Existing'),
        ('vip', 'VIP')
    ], string='Client Category')

    quote_category = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('hourly', 'Hourly'),
        ('milestone', 'Milestone Based')
    ], string='Quote Category')

    profile = fields.Char(string='Profile Name')

# from odoo import models, fields, api
#
#
# class CrmLead(models.Model):
#     _inherit = 'res.partner'
#
#     bidding_amount = fields.Char(string='Bidding status')
#
#     client_user_id = fields.Many2one('res.users', string='Client User Name')
#     # User_id= fields.Many2one('profile.profile',string='USER_ID')
#     User_id = fields.Many2one('hr.employee', string='User ID')
#     Name = fields.Many2one('hr.employee', string='Name')
#
#     # sbus = fields.Char(string="company name")
#     # sbus_id = fields.Many2one('res.company', string="Company Name")
#     date = fields.Date(string='Date')
#     # employee_name = fields.Many2one('hr.employee', string='Employee')
#
#     service_type = fields.Many2one('product.template', string='service_type')
#     bidding_status = fields.Selection([
#         ('draft', 'Draft'),
#         ('submitted', 'Submitted'),
#         ('won', 'Won'),
#         ('lost', 'Lost')
#     ], string='Bidding Status', default='draft')
#     # amount=fields.Many2one('sale.order',string="amount")
#     payment_status = fields.Selection([
#         ('sold', 'Sold'),
#         ('unsold', 'Unsold'),
#
#     ], string='Payment Status', )
#     client_category = fields.Selection([
#         ('new', 'New'),
#         ('existing', 'Existing'),
#         ('vip', 'VIP')
#     ], string='Client Category')
#     quote_category = fields.Selection([
#         ('fixed', 'Fixed Price'),
#         ('hourly', 'Hourly'),
#         ('milestone', 'Milestone Based')
#     ], string='Quote Category')
#
#     profile = fields.Many2one('bd.profile', string='profile_Name')
#

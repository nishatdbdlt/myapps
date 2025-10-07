from odoo import fields, models, api

class PreSales(models.Model):
    _name = 'pre.sales'
    _description = 'Pre Sales'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    SBUs = fields.Many2one(
        'res.company',
        string='Company_ID',
        required=True,
        default=lambda self: self.env.company,
        index=True
    )
    date = fields.Date(string='Date')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
# In your pre.sales model
    client_user_name = fields.Many2one('res.partner', string='Client/User Name')    
    name = fields.Many2one('hr.employee', string='Employee Name', tracking=True)

   
    # client_user_name = fields.Many2one('res.partner', string='Client/User Name')
    # country = fields.Char(string='Country')
    profile_name = fields.Many2one('hr.employee',string='Profile Name')
    service_type = fields.Many2one('service.type', string='Service Type')
    biding_amount = fields.Selection(
        [
            ('sold', 'Sold'),
            ('pending', 'Pending')
        ],
        string='Biding Amount',
        default='pending'  # Optional: set default value
    )

    amount_status = fields.Selection([
        ('sold', 'Sold'),
        ('unpaid', 'Unpaid')
    ], string='Amount Status')

    client_category = fields.Selection(
        [
            ('potential', 'Potential'),
            ('non_potential', 'Non-Potential')
        ],
        string='Client Category',
        default='potential'  # Optional: set a default value
    )

    quote_category = fields.Selection([
        ('apps', 'Apps'),
        ('web', 'Web'),
        
    ], string='Quote Category')


    @api.onchange('SBUs')
    def _onchange_company(self):
        """Filter users by the selected company"""
        if self.SBUs:
            return {
                'domain': {
                    'user_id': [('company_id', '=', self.SBUs.id)]
                }
            }

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """Set employee based on selected user"""
        if self.user_id:
            employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
            self.name = employee.id if employee else False

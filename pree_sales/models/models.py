from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    client_user_id = fields.Many2one(
        'res.users',
        string='Client User',
        help='The user who created this bidding record',
        index=True
    )

    bidding_amount = fields.Float(
        string='Bidding Amount',
        digits='Product Price',
        help='Amount for this bidding'
    )

    bidding_status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Bidding Status', default='draft', required=True)

    # Optional: Add a computed field to check if current user owns this bidding
    @api.depends('client_user_id')
    def _compute_is_my_bidding(self):
        for record in self:
            record.is_my_bidding = record.client_user_id == self.env.user

    is_my_bidding = fields.Boolean(
        string='My Bidding',
        compute='_compute_is_my_bidding',
        store=False
    )
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalBill(models.Model):
    _name = 'hospital.bill'
    _description = 'Hospital Bill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Bill Reference', required=True, copy=False,
                       readonly=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    bill_date = fields.Date(string='Bill Date', default=fields.Date.context_today)

    # Bill Lines
    line_ids = fields.One2many('hospital.bill.line', 'bill_id', string='Bill Lines')

    # Totals
    subtotal = fields.Float(string='Subtotal', compute='_compute_totals', store=True)
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.bill') or _('New')
        return super(HospitalBill, self).create(vals)

    @api.depends('line_ids.total')
    def _compute_totals(self):
        for record in self:
            record.subtotal = sum(line.total for line in record.line_ids)
            record.tax_amount = record.subtotal * 0.1  # 10% tax
            record.total_amount = record.subtotal + record.tax_amount

    def action_confirm(self):
        self.state = 'confirmed'

    def action_pay(self):
        self.state = 'paid'


class HospitalBillLine(models.Model):
    _name = 'hospital.bill.line'
    _description = 'Hospital Bill Line'

    bill_id = fields.Many2one('hospital.bill', string='Bill', ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.unit_price
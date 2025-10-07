from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'

    name = fields.Char(string='Appointment Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('NEW'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, tracking=True)
    # department_id = fields.Many2one('hospital.department', string='Department', tracking=True)
    appointment_date = fields.Datetime(string='Appointment Date', default=fields.Datetime.now, tracking=True)
    duration = fields.Float(string='Duration (Hours)', default=1.0)
    reason = fields.Text(string="Reason")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    consultation_fee = fields.Float(string='Consultation Fee', compute='_compute_consultation_fee',
                                  readonly=True, store=True, tracking=True)
    is_paid = fields.Boolean(string='Is Paid', default=False, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('NEW')) == _('NEW'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('NEW')
        return super(HospitalAppointment, self).create(vals)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_start(self):
        for record in self:
            record.state = 'in_progress'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    @api.depends('doctor_id')
    def _compute_consultation_fee(self):
        for rec in self:
            if rec.doctor_id and hasattr(rec.doctor_id, 'consultation_fee'):
                rec.consultation_fee = rec.doctor_id.consultation_fee
            else:
                rec.consultation_fee = 0.0

    # @api.onchange('doctor_id')
    # def _onchange_doctor_id(self):
    #     if self.doctor_id:
    #         # Set department based on doctor's department
    #         if hasattr(self.doctor_id, 'department_id'):
    #             self.department_id = self.doctor_id.department_id

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            if record.appointment_date and record.appointment_date.date() < date.today():
                raise ValidationError(_("Appointment date cannot be in the past."))

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.patient_id:
                name = f"{record.name} - {record.patient_id.name}"
            result.append((record.id, name))
        return result
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date



class HospitalMedicalRecord(models.Model):
    _name = 'hospital.medical.record'
    _description = 'Medical Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Record Reference', required=True, copy=False,
                       readonly=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    symptoms = fields.Text(string='Symptoms')
    diagnosis = fields.Text(string='Diagnosis')
    treatment = fields.Text(string='Treatment')
    prescription = fields.Text(string='Prescription')

    # Vital Signs
    temperature = fields.Float(string='Temperature (°F)')
    blood_pressure_systolic = fields.Integer(string='BP Systolic')
    blood_pressure_diastolic = fields.Integer(string='BP Diastolic')
    pulse_rate = fields.Integer(string='Pulse Rate')
    weight = fields.Float(string='Weight (kg)')
    height = fields.Float(string='Height (cm)')

    next_visit_date = fields.Date(string='Next Visit Date')
    notes = fields.Text(string='Additional Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.medical.record') or _('New')
        return super(HospitalMedicalRecord, self).create(vals)

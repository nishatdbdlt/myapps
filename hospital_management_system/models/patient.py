from email.policy import default

from stdnum.pe.ruc import to_dni

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class HospitalPatient(models.Model):
    _name='hospital.patient'
    _description = 'Hospital patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'create_date desc'

    name=fields.Char(string='patient name',required=True,tracking=True)
    patient_id=fields.Char(string='Patient_id',required=True,copy=False,readonly=True,default=lambda self:_('NEW'))
    date_of_birth=fields.Date(string='BOD',required=True)
    age=fields.Integer(string="age",compute="_compute_age",store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Group')
    phone=fields.Integer(string="phone")
    Email=fields.Char(string='email')
    address=fields.Char(string='address')
    emergency_contact=fields.Char(string="emergency_contact")
    emergency_phone=fields.Char(string="Emergency_phone")
    medical_history=fields.Char(string='medical_history')
    allergies=fields.Text(string='Allergies')
    current_medication=fields.Text(string="Current Medication")
    insurance_number=fields.Char(string='insurance number')
    # relation
    appointment_ids=fields.One2many('hospital.appointment','patient_id',string='Appointment')
    medical_record_ids=fields.One2many('hospital.medical.record','patient_id',string='medical record')
    bill_ids = fields.One2many('hospital.bill', 'patient_id', string='Hospital Bill')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('patient_id',_('New')) ==_('New'):
            vals['patient_id']=self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
            return super(HospitalPatient,self).create(vals)




    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today=date.today()
                record.age=today.year - record.date_of_birth.year - \
                           ((today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
            else:
                record.age=0

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(_('Please enter a valid email address.'))
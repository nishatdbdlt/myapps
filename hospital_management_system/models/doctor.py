
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date







class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Doctor Name', required=True, tracking=True)
    doctor_id = fields.Char(string='Doctor ID', required=True, copy=False,
                            readonly=True, default=lambda self: _('New'))
    specialization = fields.Char(string='Specialization', required=True)
    qualification = fields.Text(string='Qualification')
    experience_years = fields.Integer(string='Years of Experience')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    license_number = fields.Char(string='License Number')
    consultation_fee = fields.Float(string='Consultation Fee')

    # Relations
    department_id = fields.Many2one('hospital.department', string='Department')
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')

    # Availability
    available_days = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], string='Available Days', )

    available_time_from = fields.Float(string='Available From')
    available_time_to = fields.Float(string='Available To')

    state = fields.Selection([
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave')
    ], string='Status', default='available', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('doctor_id', _('New')) == _('New'):
            vals['doctor_id'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        return super(HospitalDoctor, self).create(vals)
from odoo import models, fields, api, _

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code', required=True)
    description = fields.Text(string='Description')
    head_doctor_id = fields.Many2one('hospital.doctor', string='Head Doctor')

    # Relations
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
    room_ids = fields.One2many('hospital.room', 'department_id', string='Rooms')

    active = fields.Boolean(string='Active', default=True)
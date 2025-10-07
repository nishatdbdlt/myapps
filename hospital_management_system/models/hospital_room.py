from dataclasses import fields

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class HospitalRoom(models.Model):
    _name = 'hospital.room'
    _description = 'Hospital Room'

    name = fields.Char(string='Room Number', required=True)
    room_type = fields.Selection([
        ('general', 'General Ward'),
        ('private', 'Private Room'),
        ('icu', 'ICU'),
        ('operation', 'Operation Theater'),
        ('emergency', 'Emergency')
    ], string='Room Type', required=True)

    capacity = fields.Integer(string='Bed Capacity', default=1)
    department_id = fields.Many2one('hospital.department', string='Department')
    floor = fields.Integer(string='Floor')

    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance')
    ], string='Status', default='available')

    daily_rent = fields.Float(string='Daily Rent')
    facilities = fields.Text(string='Facilities')
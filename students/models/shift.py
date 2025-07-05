# models/school_shift.py
from odoo import models, fields

class SchoolShift(models.Model):
    _name = 'school.shift'
    _description = 'School Shift'

    name = fields.Char(string="Shift Name", required=True)
    class_ids = fields.One2many('school.class', 'shift_id', string="Classes")

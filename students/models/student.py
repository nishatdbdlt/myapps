# models/school_student.py
from odoo import models, fields ,api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'

    name = fields.Char(string="Student Name", required=True)
    roll = fields.Char(string="Roll")
    shift_id = fields.Many2one('school.shift', string="Shift")
    class_id = fields.Many2one('school.class', string="Class")
    section_id = fields.Many2one('school.section', string="Section")
    phone = fields.Char(string="Phone")
    photo=fields.Binary(
     string='photo'
    )
    filter_id = fields.Many2one('library.student.filter', string='Filter Link')
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Group', required=True)


@api.onchange('shift_id')
def _onchange_shift_id(self):
        self.class_id = False
        self.section_id = False

@api.onchange('class_id')
def _onchange_class_id(self):
        self.section_id = False




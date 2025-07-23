# models/school_class.py
from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string="Class Name", required=True)
    shift_id = fields.Many2one('school.shift', string="Shift", required=True)
    section_ids = fields.One2many('school.section', 'class_id', string="Sections")

    class_teacher_id = fields.Many2one(
        'school.teacher',
        string='Class Teacher',
        help='The teacher responsible for this class'
    )


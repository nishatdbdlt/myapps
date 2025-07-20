# school_class_report/models/school_teacher.py
from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name        = fields.Char(string='Teacher Name', required=True)
    phone       = fields.Char(string='Phone')
    photo       = fields.Binary(string='Photo')
    email=fields.Char(string='email')
    subject_ids = fields.One2many('school.subject', 'teacher_id', string='Subjects')

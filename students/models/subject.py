# school_class_report/models/school_subject.py
from odoo import models, fields

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name        = fields.Char(string='Subject Name', required=True)
    class_id    = fields.Many2one('school.class',   string='Class',   ondelete='cascade')
    section_id  = fields.Many2one('school.section', string='Section', ondelete='cascade')
    teacher_id  = fields.Many2one('school.teacher', string='Teacher')

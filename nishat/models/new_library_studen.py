from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Info'

    name = fields.Char("Name", required=True)
    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], default='student')
    class_id = fields.Many2one('school.class', string="Class")
    section_id = fields.Many2one('school.section', string="Section")
    photo = fields.Binary("Photo")
    roll = fields.Char("Roll")
    phone = fields.Char("Phone")

from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string="Class Name", required=True)

    section = fields.Selection([
        ('golap', 'সেকশন গোলাপ'),
        ('shapla', 'সেকশন শাপলা'),
    ], string="Section", required=True)

    student_ids = fields.One2many('school.student', 'class_id', string="Students")
    photo = fields.Binary(string='Image')

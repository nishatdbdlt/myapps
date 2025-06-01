from odoo import models, fields, api

class EduStudent(models.Model):
    _name = 'edu.student'
    _description = 'Student'

    name = fields.Char(required=True)
    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')], required=True)
    roll = fields.Char()
    phone = fields.Char()
    photo = fields.Binary()
    lid = fields.Char(string="Library ID")
    class_id = fields.Many2one('edu.class', string='Class')
    section_id = fields.Many2one('edu.section', string='Section')

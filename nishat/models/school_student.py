from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'
    _rec_name = 'name'

    name = fields.Char(string="Student Name", required=True)
    roll = fields.Char(string="Roll Number")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    photo = fields.Image(string="Photo", max_width=100, max_height=100)

    class_id = fields.Many2one('school.class', string="Class", required=True, ondelete='cascade')
    section_id = fields.Many2one('school.section', string="Section")

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], string="User Type")

    is_active = fields.Boolean(string="Active", default=True)

    active_member_id = fields.Many2one('edu.active.member', string="Active Member")

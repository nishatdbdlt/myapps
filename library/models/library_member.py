from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class EduActiveMember(models.Model):
    _name = 'edu.member'
    _description = 'Library Member Filter'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], string="User Type")

    select_class_id = fields.Many2one('school.class', string="Select Class")

    filtered_student_ids = fields.One2many('school.student', compute='_compute_filtered_students', string="Students")
    # roll = fields.Char(string="Roll Number")  # ✅ Add this line
    # name=fields.Char(string="name")

    @api.depends('user_type', 'select_class_id')
    def _compute_filtered_students(self):
        for rec in self:
            if rec.user_type == 'student' and rec.select_class_id:
                rec.filtered_student_ids = self.env['school.student'].search([
                    ('class_id', '=', rec.select_class_id.id)
                ])
            else:
                rec.filtered_student_ids = False

    def get_students(self):
        for rec in self:
            _logger.info(f"User Type: {rec.user_type}, Class: {rec.select_class_id.name}")
        return True

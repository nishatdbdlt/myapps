from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class EduActiveMember(models.TransientModel):
    _name = 'edu.member'
    _description = 'Library Member Filter'
    # _rec_name = 'user_type'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ], string="User Type")

    section_id = fields.Many2one('edu.section', string='Section')
    select_class_id = fields.Many2one('edu.class', string="Select Class")

    filtered_student_ids = fields.One2many(
        'manage.user.student',
        compute='_compute_filtered_students',
        string="Students",
        store=False
    )

    @api.depends('user_type', 'select_class_id', 'section_id')
    def _compute_filtered_students(self):
        for rec in self:
            if rec.user_type == 'student' and rec.select_class_id and rec.section_id:
                rec.filtered_student_ids = self.env['manage.user.student'].search([
                    ('student_class_id', '=', rec.select_class_id.id),
                    ('section_id', '=', rec.section_id.id),
                ])
            else:
                rec.filtered_student_ids = False

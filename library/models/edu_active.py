from odoo import models, fields, api

class EduActiveMember(models.Model):
    _name = 'edu.active.member'
    _description = 'Active Member'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    select_class_id = fields.Many2one('school.class', string="Class", required=True)

    # library_id = fields.Many2one('school.student', string="Library ID")  # correct type here
    # temp_library_id = fields.Char(string="Library Temporary ID")
    # library_fee = fields.Float(string="Library Fee")

    # student_ids = fields.One2many('school.student', compute='_compute_students', string="Students")
    student_ids = fields.One2many('school.student', compute='_compute_students', string="Students")

    @api.depends('user_type', 'select_class_id')
    def _compute_students(self):
        for rec in self:
            if rec.user_type == 'student' and rec.select_class_id:
                rec.student_ids = self.env['school.student'].search([
                    ('class_id', '=', rec.select_class_id.id),
                    ('is_active_member', '=', True)  # Only active members
                ])
            else:
                rec.student_ids = False

    def action_show_students(self):
        self.ensure_one()
        return {
            'name': 'Active Students',
            'type': 'ir.actions.act_window',
            'res_model': 'edu.member',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [
                ('user_type', '=', 'student'),
                ('class_id', '=', self.select_class_id.id),
                ('is_active_member', '=', True)  # Filter active only
            ],
        }


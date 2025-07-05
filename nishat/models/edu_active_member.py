from odoo import models, fields, api


class EduActiveMember(models.TransientModel):
    _name = 'edu.active.member'
    _description = 'Active Member'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    select_class_id = fields.Many2one('edu.class', string="Class", )
    # select_class=fields.Char(string='class')

    student_ids = fields.One2many('manage.user.student', compute='_compute_students', string="Students")

    # is_active = fields.Boolean(string="Active", default=True)

    # student_ids =fields.Char(string="student")

    @api.depends('user_type', 'select_class_id')
    def _compute_students(self):
        for rec in self:
            if rec.user_type == 'student' and rec.select_class_id:
                rec.student_ids = self.env['manage.user.student'].search([
                    ('student_class_id', '=', rec.select_class_id.id)
                ])
            else:
                rec.student_ids = False

    def action_show_students(self):
        self.ensure_one()
        return {
            'name': 'Students',
            'type': 'ir.actions.act_window',
            'res_model': 'manage.user.student',  # Change if your student model is different
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [
                ('user_type', '=', 'student'),
                ('class_id', '=', self.select_class_id.id)
            ],
        }

    # all needed after connection
    # need model school.student  school.class
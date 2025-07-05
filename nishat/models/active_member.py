from odoo import models, fields, api

class EduActiveMember(models.Model):
    _name = 'edu.active.member'
    _description = 'Active Member in Education System'
    _rec_name = 'user_type'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    select_class_id = fields.Many2one('school.class', string="Class")

    student_ids = fields.Many2many(
        'school.student',
        string="Students",
        compute='_compute_student_ids',
        store=False
    )

    @api.depends('user_type', 'select_class_id')
    def _compute_student_ids(self):
        for rec in self:
            domain = []
            if rec.user_type:
                domain.append(('user_type', '=', rec.user_type))
            if rec.select_class_id:
                domain.append(('class_id', '=', rec.select_class_id.id))
            rec.student_ids = self.env['school.student'].search(domain)

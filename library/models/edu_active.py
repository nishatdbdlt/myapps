from odoo import models, fields, api

class EduActiveMember(models.Model):
    _name = 'edu.active.member'
    _description = 'Active Member'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    select_class_id = fields.Many2one('school.class', string="Class", required=True)

    student_ids = fields.One2many('school.student', compute='_compute_students', string="Students")
    # @api.depends('user_type', 'select_class_id')
    # def _compute_student_html(self):
    #     for rec in self:
    #         students = self.env['school.student'].search([
    #             ('class_id', '=', rec.select_class_id.id)
    #         ])
    #         html = "<div>"
    #         for student in students:
    #             html += f"""
    #                 <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
    #                     <img src="data:image/png;base64,{student.photo or ''}"
    #                          style="width:80px; height:80px; object-fit:cover; float:left; margin-right:10px;"/>
    #                     <strong>Name:</strong> {student.name}<br/>
    #                     <strong>Roll:</strong> {student.roll}<br/>
    #                     <strong>Phone:</strong> {student.phone}<br/>
    #                     <div style="clear:both;"></div>
    #                 </div>
    #             """
    #         html += "</div>"
    #         rec.student_html = html

    @api.depends('user_type', 'select_class_id')
    def _compute_students(self):
        for rec in self:
            if rec.user_type == 'student' and rec.select_class_id:
                rec.student_ids = self.env['school.student'].search([
                    ('class_id', '=', rec.select_class_id.id)
                ])
            else:
                rec.student_ids = False

    def action_show_students(self):
        self.ensure_one()
        return {
            'name': 'Students',
            'type': 'ir.actions.act_window',
            'res_model': 'school.student',  # Change if your student model is different
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [
                ('user_type', '=', 'student'),
                ('class_id', '=', self.select_class_id.id)
            ],
        }





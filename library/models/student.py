from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name = fields.Char(string="Name")
    photo = fields.Binary(string="Photo")
    roll = fields.Char(string="Roll")
    class_id = fields.Many2one('school.class', string="Class")
    section_id = fields.Many2one('school.section', string="Section")
    phone = fields.Char(string="Phone")
    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", default='student')

    is_active_member = fields.Boolean(string="Active", default=True)

    show_library_fields = fields.Boolean(string="Show Library Fields", default=False)

    library_id = fields.Integer(string="Library ID")
    temp_library_id = fields.Char(string="Library Temporary ID")
    library_fee = fields.Float(string="Library Fee")

    @api.depends('class_id')
    def _compute_sections(self):
        for rec in self:
            rec.section_ids = self.env['edu.section'].search(
                [('class_id', '=', rec.class_id.id)]) if rec.class_id else False

    @api.depends('user_type', 'class_id', 'selected_section_id')
    def _compute_students(self):
        for rec in self:
            domain = [('user_type', '=', rec.user_type)]
            if rec.class_id:
                domain.append(('class_id', '=', rec.class_id.id))
            if rec.selected_section_id:
                domain.append(('section_id', '=', rec.selected_section_id.id))
            rec.student_ids = self.env['edu.student'].search(domain)

    def action_activate_student(self):
        for student in self:
            student.is_active = True

    def action_deactivate_student(self):
        for student in self:
            student.is_active = False

    # def toggle_library_fields(self):
    #     for record in self:
    #         record.show_library_fields = not record.show_library_fields

    def open_library_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manage Library Info',
            'res_model': 'library.member.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_id': self,
                'default_library_id': self.library_id,
                'default_temp_library_id': self.temp_library_id,
                'default_library_fee': self.library_fee,
            }
        }

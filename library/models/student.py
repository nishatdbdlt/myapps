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


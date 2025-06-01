from odoo import models, fields, api

class EduActiveMember(models.TransientModel):
    _name = 'edu.active.member'
    _description = 'Active Member Wizard'

    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')], string="User Type", required=True)
    class_id = fields.Many2one('edu.class', string="Class", required=True)
    section_id = fields.Many2one('edu.section', string="Section")

    section_ids = fields.One2many('edu.section', compute='_compute_sections')
    student_ids = fields.One2many('edu.student', compute='_compute_students')

    selected_section_id = fields.Many2one('edu.section', string="Selected Section")

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

from odoo import models, fields, api

class StudentIDCardWizard(models.TransientModel):
    _name = 'student.id.card.wizard'
    _description = 'Student ID Card Wizard'

    shift_id = fields.Many2one('school.shift', string="Shift", required=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)
    section_id = fields.Many2one('school.section', string="Section", required=True)
    student_id = fields.Many2one('school.student', string="Student", required=True)

    @api.onchange('shift_id')
    def _onchange_shift_id(self):
        if self.shift_id:
            classes = self.env['school.class'].search([('shift_id', '=', self.shift_id.id)])
            return {'domain': {'class_id': [('id', 'in', classes.ids)]}}
        return {'domain': {'class_id': []}}

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            sections = self.env['school.section'].search([('class_id', '=', self.class_id.id)])
            return {'domain': {'section_id': [('id', 'in', sections.ids)]}}
        return {'domain': {'section_id': []}}

    @api.onchange('section_id')
    def _onchange_section_id(self):
        if self.shift_id and self.class_id and self.section_id:
            students = self.env['school.student'].search([
                ('shift_id', '=', self.shift_id.id),
                ('class_id', '=', self.class_id.id),
                ('section_id', '=', self.section_id.id),
            ])
            return {'domain': {'student_id': [('id', 'in', students.ids)]}}
        return {'domain': {'student_id': []}}

    def action_print_id_card(self):
        return self.env.ref('students.action_report_student_id').report_action(self.student_id)

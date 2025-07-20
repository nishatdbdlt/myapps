# models/library_student_wizard.py
from odoo import models, fields, api

class LibraryStudentWizard(models.TransientModel):
    _name = 'library.student.wizard'
    _description = 'Student Filter Wizard'

    shift_id = fields.Many2one(
        'school.shift', string='Shift', required=True)
    class_id = fields.Many2one(
        'school.class', string='Class',
        domain="[('shift_id','=',shift_id)]", required=True,readonly=False)
    section_id = fields.Many2one(
        'school.section', string='Section',
        domain="[('class_id','=',class_id)]", required=True)
    students_ids = fields.One2many(
        comodel_name='school.student',
        inverse_name='filter_id',
        string='Students',
        compute='_compute_students',
        store=False,
    )

    @api.onchange('shift_id')
    def _onchange_shift(self):
        # Tell the client to clear class and section fields
        return {
            'value': {
                'class_id': False,
                'section_id': False,
            }
        }

    @api.onchange('class_id')
    def _onchange_class(self):
        # Tell the client to clear the section field
        return {
            'value': {
                'section_id': False,
            }
        }

    @api.depends('shift_id', 'class_id', 'section_id')
    def _compute_students(self):
        for record in self:
            if record.shift_id and record.class_id and record.section_id:
                record.students_ids = self.env['school.student'].search([
                    ('shift_id', '=', record.shift_id.id),
                    ('class_id', '=', record.class_id.id),
                    ('section_id', '=', record.section_id.id),
                ])
            else:
                record.students_ids = False

    def action_print_pdf(self):
        return self.env.ref('students.action_report_student').report_action(self)

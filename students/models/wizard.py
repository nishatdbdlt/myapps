# models/library_student_wizard.py
from odoo import models, fields, api

class LibraryStudentWizard(models.TransientModel):
    _name = 'library.student.wizard'
    _description = 'Student Filter Wizard'

    shift_id = fields.Many2one('school.shift', string='Shift', required=True)
    class_id = fields.Many2one(
        'school.class', string='Class',
        domain="[('shift_id','=',shift_id)]", required=True)
    section_id = fields.Many2one(
        'school.section', string='Section',
        domain="[('class_id','=',class_id)]", required=True)
    students_ids = fields.One2many(
        comodel_name='school.student',
        inverse_name='filter_id',  # This will be virtual, just for placeholder
        string='Students',
        compute='_compute_students',
        store=False,
    )

    @api.onchange('shift_id')
    def _onchange_shift(self):
        self.class_id = False
        self.section_id = False

    @api.onchange('class_id')
    def _onchange_class(self):
        self.section_id = False

    # def action_show_students(self):
    #     self.ensure_one()
    #     domain = [
    #         ('shift_id', '=', self.shift_id.id),
    #         ('class_id', '=', self.class_id.id),
    #         ('section_id', '=', self.section_id.id),
    #     ]
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Filtered Students',
    #         'res_model': 'school.student',
    #         'view_mode': 'tree,form',
    #         'domain': domain,
    #         'target': 'current',
    #     }

    @api.depends('shift_id', 'class_id', 'section_id')
    def _compute_students(self):
        for record in self:
            if record.shift_id and record.class_id and record.section_id:
                students = self.env['school.student'].search([
                    ('shift_id', '=', record.shift_id.id),
                    ('class_id', '=', record.class_id.id),
                    ('section_id', '=', record.section_id.id),
                ])
                record.students_ids = students
            else:


                   record.students_ids = False

    def action_print_pdf(self):
        return self.env.ref('students.report_student_wizard_pdf').report_action(self)



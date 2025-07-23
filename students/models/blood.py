from odoo import models, fields, api

class StudentFilterWizard(models.TransientModel):
    _name = 'student.filter.wizard'
    _description = 'Filter Students by Shift, Class, Section and Blood Group'

    shift_id = fields.Many2one('school.shift', string='Shift', required=True)
    class_id = fields.Many2one('school.class', string='Class', domain="[('shift_id','=',shift_id)]", required=True)
    section_id = fields.Many2one('school.section', string='Section', domain="[('class_id','=',class_id)]", required=True)
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Group', required=True)

    student_ids = fields.Many2many(
        'school.student', string='Filtered Students',
        compute='_compute_students',
        store=False
    )

    @api.onchange('shift_id')
    def _onchange_shift_id(self):
        self.class_id = False
        self.section_id = False

    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.section_id = False

    @api.depends('shift_id', 'class_id', 'section_id', 'blood_group')
    def _compute_students(self):
        for record in self:
            if record.shift_id and record.class_id and record.section_id and record.blood_group:
                domain = [
                    ('shift_id', '=', record.shift_id.id),
                    ('class_id', '=', record.class_id.id),
                    ('section_id', '=', record.section_id.id),
                    ('blood_group', '=', record.blood_group)
                ]
                record.student_ids = self.env['school.student'].search(domain)
            else:
                record.student_ids = self.env['school.student'].browse([])  # empty recordset

    def action_print_pdf(self):
        return self.env.ref('students.action_report_filtered_students').report_action(self)


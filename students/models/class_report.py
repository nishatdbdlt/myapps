# school_class_report/models/class_report_wizard.py

from odoo import api, fields, models

class ClassReportWizard(models.TransientModel):
    _name = 'class.report.wizard'
    _description = 'Class Report Wizard'

    class_id   = fields.Many2one('school.class',   string='Class',   required=True)
    section_id = fields.Many2one('school.section', string='Section', required=True)
    line_ids   = fields.One2many('class.report.line', 'wizard_id', string='Subjects & Teachers')

    class_teacher_id = fields.Many2one(
        'school.teacher',
        string='Class Teacher',
        readonly=True,
        compute='_compute_class_teacher'


    )

    @api.depends('class_id')
    def _compute_class_teacher(self):
        for wiz in self:
            wiz.class_teacher_id = wiz.class_id.class_teacher_id or False

    @api.onchange('class_id')
    def _onchange_class(self):
        self.section_id = False

    @api.onchange('class_id', 'section_id')
    def _compute_lines(self):
        self.line_ids = [(5, 0, 0)]
        if self.class_id and self.section_id:
            subjects = self.env['school.subject'].search([
                ('class_id', '=', self.class_id.id),
                ('section_id', '=', self.section_id.id)
            ])
            lines = [(0, 0, {
                'subject_id': sub.id,
                'teacher_id': sub.teacher_id.id if sub.teacher_id else False,
            }) for sub in subjects]
            self.line_ids = lines

    # def action_get_report(self):
    #     # লাইন গুলো আপডেট
    #     self._compute_lines()
    #     # PDF রিপোর্ট রিটার্ন
    #     return self.env.ref('students.report_summary_report').report_action(self)

    def action_get_report(self):
        self._compute_lines()
        return self.env.ref('students.action_report_class_teacher').report_action(self)




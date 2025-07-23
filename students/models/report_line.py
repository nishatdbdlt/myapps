# school_class_report/models/class_report_line.py
from odoo import fields, models

class ClassReportLine(models.TransientModel):
    _name = 'class.report.line'
    _description = 'Class Report Line'

    wizard_id  = fields.Many2one('class.report.wizard', string='Wizard', ondelete='cascade')
    subject_id = fields.Many2one('school.subject', string='Subject', readonly=True)
    teacher_id = fields.Many2one('school.teacher', string='Teacher', readonly=True)

# models/school_section.py
from odoo import models, fields

class SchoolSection(models.Model):
    _name = 'school.section'
    _description = 'School Section'

    name = fields.Char(string="Section Name", required=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)

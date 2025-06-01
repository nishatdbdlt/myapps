
from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(string='Class Name', required=True)
    section = fields.Selection([
        ('golap', 'Golap'),
        ('shapla', 'Shapla'),
        ('lotus', 'Lotus'),
    ], string='Section', required=True)

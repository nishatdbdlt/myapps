from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class Info'

    name = fields.Char(string='Class Name')

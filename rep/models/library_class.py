from odoo import models, fields, api

class EduClass(models.Model):
    _name = 'edu.class'
    _description = 'Class'

    name = fields.Char(required=True)
    section_ids = fields.One2many('edu.section', 'class_id', string='Sections')

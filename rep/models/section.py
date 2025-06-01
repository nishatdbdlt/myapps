from odoo import models, fields, api

class EduSection(models.Model):
    _name = 'edu.section'
    _description = 'Section'

    name = fields.Char(required=True)
    class_id = fields.Many2one('edu.class', string='Class', required=True)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalMedicine(models.Model):
    _name = 'hospital.medicine'
    _description = 'Hospital Medicine'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Medicine Name', required=True)
    generic_name = fields.Char(string='Generic Name')
    medicine_type = fields.Selection([
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops')
    ], string='Type', required=True)

    manufacturer = fields.Char(string='Manufacturer')
    strength = fields.Char(string='Strength')
    unit_price = fields.Float(string='Unit Price')
    stock_quantity = fields.Integer(string='Stock Quantity')
    reorder_level = fields.Integer(string='Reorder Level', default=10)

    expiry_date = fields.Date(string='Expiry Date')
    batch_number = fields.Char(string='Batch Number')

    description = fields.Text(string='Description')
    side_effects = fields.Text(string='Side Effects')

    active = fields.Boolean(string='Active', default=True)
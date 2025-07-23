from odoo import models, fields

class Vendor(models.Model):
    _name = 'smartstock.vendor'
    _description = 'Vendor'

    name = fields.Char(string="Vendor Name", required=True)
    contact_person = fields.Char(string="Contact Person")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    active = fields.Boolean(default=True)

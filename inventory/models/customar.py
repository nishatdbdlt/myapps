from odoo import models, fields

class Customer(models.Model):
    _name = 'smartstock.customer'
    _description = 'Customer'

    name = fields.Char(string="Customer Name", required=True)
    contact_person = fields.Char(string="Contact Person")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    active = fields.Boolean(default=True)

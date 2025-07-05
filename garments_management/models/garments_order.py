from odoo import models, fields

class GarmentsOrder(models.Model):
    _name = 'garments.order'
    _description = 'Garments Customer Order'

    name = fields.Char(string='Order Number', required=True)
    customer_name = fields.Char(string='Customer Name', required=True)
    product_type = fields.Selection([
        ('shirt', 'Shirt'),
        ('pant', 'Pant'),
        ('jacket', 'Jacket'),
        ('others', 'Others')
    ], string='Product Type', required=True)

    quantity = fields.Integer(string='Quantity', required=True)
    delivery_date = fields.Date(string='Delivery Date', required=True)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Production'),
        ('done', 'Done'),
        ('delivered', 'Delivered')
    ], string='Order Status', default='draft')

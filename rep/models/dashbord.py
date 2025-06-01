from odoo import models, fields

class RetailDashboard(models.Model):
    _name = 'retail.dashboard'
    _description = 'Retail Dashboard'

    total_sales = fields.Float(string='Total Sales', readonly=True)
    total_inventory = fields.Integer(string='Total Inventory Items', readonly=True)
    pending_deliveries = fields.Integer(string='Pending Deliveries', readonly=True)
    employee_count = fields.Integer(string='Active Employees', readonly=True)

# manage_retail_erp/models/payroll.py

from odoo import models, fields, api

class RetailPayroll(models.Model):
    _name = 'retail.payroll'
    _description = 'Retail Payroll Management'

    employee_name = fields.Char(string='Employee Name', required=True)
    employee_id = fields.Char(string='Employee ID')
    salary = fields.Float(string='Basic Salary', required=True)
    bonus = fields.Float(string='Bonus')
    total_payable = fields.Float(string='Total Payable', compute='_compute_total', store=True)
    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid')
    ], string='Payment Status', default='unpaid')
    payment_date = fields.Date(string='Payment Date')

    @api.depends('salary', 'bonus')
    def _compute_total(self):
        for rec in self:
            rec.total_payable = rec.salary + rec.bonus

# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class SalesKPI(models.Model):
    _name = 'sales.kpi'
    _description = 'Sales KPI Tracking'
    _order = 'date desc, team_id'

    name = fields.Char('Name', compute='_compute_name', store=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', required=True)
    date = fields.Date('Month', required=True, default=fields.Date.today)

    # Sales Goals & Actuals
    sales_goal = fields.Float('Sales Goal', digits=(16, 2))
    actual_sales = fields.Float('Actual Sales', digits=(16, 2))
    sales_variance = fields.Float('Sales Variance', compute='_compute_variances', store=True, digits=(16, 2))

    # Revenue
    green_revenue = fields.Float('Green Sales Revenue', digits=(16, 2))

    # Balances
    sales_balance = fields.Float('Sales Balance', compute='_compute_balances', store=True, digits=(16, 2))
    accumulated_sales_balance = fields.Float('Accumulated Sales Balance', digits=(16, 2))

    # Operations
    operation_goal = fields.Float('Operation Goal', digits=(16, 2))
    actual_operation = fields.Float('Actual Operation', digits=(16, 2))
    operation_balance = fields.Float('Operation Balance', compute='_compute_balances', store=True, digits=(16, 2))
    accumulated_operation_balance = fields.Float('Accumulated Operation Balance', digits=(16, 2))

    # Special Orders
    cancelled_order = fields.Float('Cancelled Order', digits=(16, 2))
    internal_special_order = fields.Float('Internal Special Order', digits=(16, 2))
    forward_sales = fields.Float('Forward Sales (June only)', digits=(16, 2))

    # Delivery & Invoice
    delivered = fields.Float('Delivered', digits=(16, 2))
    fully_invoiced = fields.Float('Fully Invoiced', digits=(16, 2))

    # WIP & NRA
    wip_nra = fields.Float('WIP, NRA', digits=(16, 2))

    @api.depends('team_id', 'date')
    def _compute_name(self):
        for record in self:
            if record.team_id and record.date:
                month_str = record.date.strftime('%B %Y')
                record.name = f"{record.team_id.name} - {month_str}"
            else:
                record.name = "New KPI"

    @api.depends('sales_goal', 'actual_sales')
    def _compute_variances(self):
        for record in self:
            record.sales_variance = record.actual_sales - record.sales_goal

    @api.depends('sales_goal', 'actual_sales', 'operation_goal', 'actual_operation')
    def _compute_balances(self):
        for record in self:
            record.sales_balance = record.actual_sales - record.sales_goal
            record.operation_balance = record.actual_operation - record.operation_goal

    def action_open_details(self):
        """Open detailed view for this KPI record"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'KPI Details - {self.name}',
            'res_model': 'sales.kpi',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    kpi_ids = fields.One2many('sales.kpi', 'team_id', string='KPI Records')
    is_all_team = fields.Boolean('Is All Team', default=False,
                                 help="Check if this represents combined data from all teams")
    parent_company = fields.Char('Parent Company', help="e.g., BETOPIA GROUP $, BETOPIA GROUP বাংলা")

    def action_view_kpis(self):
        """Open KPI records for this team"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'KPIs - {self.name}',
            'res_model': 'sales.kpi',
            'domain': [('team_id', '=', self.id)],
            'view_mode': 'tree,form,pivot,graph',
            'context': {'default_team_id': self.id},
        }
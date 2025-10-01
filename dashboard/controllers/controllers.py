# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class KPIDashboardController(http.Controller):

    @http.route('/dashboard/data', type='json', auth='user')
    def get_dashboard_data(self, year=None):
        """Get dashboard data for a specific year"""
        if not year:
            year = request.env.context.get('tz_offset', 0)

        # Fetch KPI data
        kpi_obj = request.env['sales.kpi']
        kpis = kpi_obj.search([])

        data = []
        for kpi in kpis:
            data.append({
                'id': kpi.id,
                'team_id': kpi.team_id.id,
                'team_name': kpi.team_id.name,
                'date': kpi.date.strftime('%Y-%m-%d') if kpi.date else '',
                'sales_goal': kpi.sales_goal,
                'actual_sales': kpi.actual_sales,
                'sales_variance': kpi.sales_variance,
                'green_revenue': kpi.green_revenue,
                'sales_balance': kpi.sales_balance,
                'accumulated_sales_balance': kpi.accumulated_sales_balance,
                'operation_goal': kpi.operation_goal,
                'actual_operation': kpi.actual_operation,
                'operation_balance': kpi.operation_balance,
                'accumulated_operation_balance': kpi.accumulated_operation_balance,
            })

        return {'status': 'success', 'data': data}

    @http.route('/kpi/dashboard/export', type='http', auth='user')
    def export_dashboard(self, **kwargs):
        """Export dashboard data to Excel"""
        # This can be implemented later with xlsxwriter or openpyxl
        pass
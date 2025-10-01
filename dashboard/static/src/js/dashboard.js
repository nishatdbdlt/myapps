/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class EmployeeKPIDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.rpc = useService("rpc");

        this.state = useState({
            kpiData: [],
            summary: {},
            employees: [],
            loading: true,
            selectedYear: new Date().getFullYear(),
            selectedEmployee: null,
            selectedRoleType: null,
            showFilters: false,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        try {
            this.state.loading = true;

            const dashboardData = await this.rpc('/employee/kpi/dashboard/data', {
                year: this.state.selectedYear,
                employee_id: this.state.selectedEmployee,
                role_type: this.state.selectedRoleType,
            });

            if (dashboardData.status === 'success') {
                this.state.kpiData = dashboardData.data;
            }

            const summaryData = await this.rpc('/employee/kpi/dashboard/summary', {
                year: this.state.selectedYear,
            });

            if (summaryData.status === 'success') {
                this.state.summary = summaryData.summary;
            }

            const employeesData = await this.rpc('/employee/kpi/dashboard/employees');

            if (employeesData.status === 'success') {
                this.state.employees = employeesData.employees;
            }

        } catch (error) {
            console.error("Error loading dashboard data:", error);
        } finally {
            this.state.loading = false;
        }
    }

    getMonthsList() {
        const months = [];
        for (let i = 0; i < 12; i++) {
            const date = new Date(this.state.selectedYear, i, 1);
            months.push(date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }));
        }
        return months;
    }

    formatCurrency(value) {
        if (!value) return '৳0';
        const formatted = Math.abs(value).toLocaleString('en-US', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
        });
        return value < 0 ? `-৳${formatted}` : `৳${formatted}`;
    }

    toggleFilters() {
        this.state.showFilters = !this.state.showFilters;
    }

    async onYearChange(event) {
        this.state.selectedYear = parseInt(event.target.value);
        await this.loadData();
    }

    async onEmployeeChange(event) {
        this.state.selectedEmployee = event.target.value ? parseInt(event.target.value) : null;
        await this.loadData();
    }

    async onRoleTypeChange(event) {
        this.state.selectedRoleType = event.target.value || null;
        await this.loadData();
    }

    async clearFilters() {
        this.state.selectedEmployee = null;
        this.state.selectedRoleType = null;
        await this.loadData();
    }

    async refreshData() {
        await this.loadData();
    }

    getYearOptions() {
        const currentYear = new Date().getFullYear();
        const years = [];
        for (let i = currentYear - 2; i <= currentYear + 1; i++) {
            years.push(i);
        }
        return years;
    }
}
           registry.category("actions").add("betopia_kpi_dashboard", (env, services) => {
    return {
        type: "ir.actions.client",
        tag: "betopia_kpi_dashboard",
        // Your action configuration
    };
});



EmployeeKPIDashboard.template = "dashboard.BetopiaKPIDashboard";
registry.category("actions").add("dashboard", EmployeeKPIDashboard);

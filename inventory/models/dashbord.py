from odoo import models, fields, api

class SmartStockDashboard(models.TransientModel):
    _name = 'smartstock.dashboard'
    _description = 'SmartStock Dashboard'

    total_products = fields.Integer(string="Total Products", compute='_compute_stats')
    low_stock_products = fields.Integer(string="Low Stock Products", compute='_compute_stats')
    total_vendors = fields.Integer(string="Total Vendors", compute='_compute_stats')
    total_customers = fields.Integer(string="Total Customers", compute='_compute_stats')
    total_purchase_orders = fields.Integer(string="Total Purchase Orders", compute='_compute_stats')
    total_sale_orders = fields.Integer(string="Total Sale Orders", compute='_compute_stats')

    @api.depends()
    def _compute_stats(self):
        product_model = self.env['smartstock.product']
        vendor_model = self.env['smartstock.vendor']
        customer_model = self.env['smartstock.customer']
        purchase_model = self.env['smartstock.purchase.order']
        sale_model = self.env['smartstock.sale.order']

        self.total_products = product_model.search_count([])
        self.low_stock_products = product_model.search_count([('quantity_on_hand', '<', 'minimum_qty')])
        self.total_vendors = vendor_model.search_count([])
        self.total_customers = customer_model.search_count([])
        self.total_purchase_orders = purchase_model.search_count([])
        self.total_sale_orders = sale_model.search_count([])


# Chart.js গ্রাফের জন্য ডাটা দিবে এই ক্লাস:
class SmartProduct(models.Model):
    _inherit = 'smartstock.product'

    @api.model
    def get_dashboard_data(self):
        categories = self.env['smartstock.product.category'].search([])
        labels = []
        quantities = []
        for cat in categories:
            qty = sum(cat.product_ids.mapped('quantity_on_hand'))
            labels.append(cat.name)
            quantities.append(qty)
        return {
            'categories': labels,
            'quantities': quantities,
        }

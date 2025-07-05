from odoo import models, fields

class ProductionReport(models.Model):
    _name = 'garment.production.report'
    _description = 'Production Analytics'
    _auto = False  # SQL ভিউ বেসড রিপোর্ট

    product_id = fields.Many2one('garment.product', 'Product')
    total_quantity = fields.Float('Total Produced')
    avg_wastage = fields.Float('Avg Wastage %')

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW garment_production_report AS
            SELECT 
                MIN(p.id) AS id,
                p.product_id,
                SUM(p.quantity) AS total_quantity,
                AVG(p.wastage) AS avg_wastage
            FROM garment_production p
            GROUP BY p.product_id
        """)
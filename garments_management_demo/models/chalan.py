from odoo import models, fields

class GarmentChallan(models.Model):
    _name = 'garment.challan'
    _description = 'Garment Challan'

    name = fields.Char(string='Challan No', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Challan Date', default=fields.Date.today)
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True
    )


    challan_line_ids = fields.One2many('garment.challan.line', 'challan_id', string='Challan Lines')
    note = fields.Text(string='Note')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('delivered', 'Delivered'),
    ], default='draft', string='Status')

    def action_deliver(self):
        self.write({'state': 'delivered'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def _generate_challan_number(self):
        return self.env['ir.sequence'].next_by_code('garment.challan') or 'New'

    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self._generate_challan_number()
        return super(GarmentChallan, self).create(vals)


class GarmentChallanLine(models.Model):
    _name = 'garment.challan.line'
    _description = 'Garment Challan Line'

    challan_id = fields.Many2one('garment.challan', string='Challan')

    # ✅ Important: Use product.template (not product.product)
    product_id = fields.Many2one('product.template', string='Product', required=True)

    quantity = fields.Float(string='Quantity', required=True)

    # ✅ This works in Odoo 17
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             related='product_id.uom_id', store=True, readonly=True)
from odoo import models, fields, api


class GarmentChallan(models.Model):
    _name = 'garment.challan'
    _description = 'Garment Challan'

    name = fields.Char(string='Challan No', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Challan Date', default=fields.Date.today)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    challan_line_ids = fields.One2many('garment.challan.line', 'challan_id', string='Challan Lines')
    note = fields.Text(string='Note')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('delivered', 'Delivered'),
    ], default='draft', string='Status')

    total_quantity = fields.Float(string='Total Quantity', compute='_compute_totals', store=True)
    total_delivered_quantity = fields.Float(string='Delivered Quantity', compute='_compute_totals', store=True)
    overall_delivery_percentage = fields.Float(string='Delivery %', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    def action_deliver(self):
        self.write({'state': 'delivered'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def _generate_challan_number(self):
        return self.env['ir.sequence'].next_by_code('garment.challan') or 'New'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self._generate_challan_number()
        return super(GarmentChallan, self).create(vals)

    @api.depends('challan_line_ids.quantity', 'challan_line_ids.delivered_quantity', 'challan_line_ids.price_subtotal')
    def _compute_totals(self):
        for rec in self:
            total_qty = sum(line.quantity for line in rec.challan_line_ids)
            total_delivered = sum(line.delivered_quantity for line in rec.challan_line_ids)
            total_amount = sum(line.price_subtotal for line in rec.challan_line_ids)

            rec.total_quantity = total_qty
            rec.total_delivered_quantity = total_delivered
            rec.overall_delivery_percentage = (total_delivered / total_qty * 100) if total_qty else 0.0
            rec.total_amount = total_amount


class GarmentChallanLine(models.Model):
    _name = 'garment.challan.line'
    _description = 'Garment Challan Line'

    challan_id = fields.Many2one('garment.challan', string='Challan')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    delivered_quantity = fields.Float(string='Delivered Quantity', required=True, default=0.0)

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure',
                             related='product_id.uom_id', store=True, readonly=True)

    unit_price = fields.Float(string='Unit Price', default=0.0)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
    delivery_percentage = fields.Float(string='Delivery %', compute='_compute_delivery_percentage', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.unit_price = rec.product_id.list_price

    @api.depends('delivered_quantity', 'unit_price')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.unit_price * rec.delivered_quantity

    @api.depends('quantity', 'delivered_quantity')
    def _compute_delivery_percentage(self):
        for rec in self:
            rec.delivery_percentage = (rec.delivered_quantity / rec.quantity * 100) if rec.quantity else 0.0

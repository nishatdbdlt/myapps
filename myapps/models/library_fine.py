# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class LibraryFine(models.Model):
    _name = 'library.fine'
    _description = 'Library Fine'
    _order = 'date_created desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char('Reference', copy=False, readonly=True)
    member_id = fields.Many2one('library.member', 'Member', required=True, tracking=True)
    book_id = fields.Many2one('library.book', 'Book', tracking=True)
    borrow_id = fields.Many2one('library.borrow', 'Borrow Record', tracking=True)
    return_id = fields.Many2one('library.return', 'Return Record', tracking=True)

    # Fine Details
    fine_type = fields.Selection([
        ('overdue', 'Overdue Fine'),
        ('damage', 'Damage Fine'),
        ('lost', 'Lost Book Fine'),
        ('membership', 'Membership Fine'),
        ('other', 'Other Fine')
    ], 'Fine Type', required=True, default='overdue', tracking=True)

    amount = fields.Float('Fine Amount', required=True, tracking=True)
    paid_amount = fields.Float('Paid Amount', tracking=True, default=0.0)
    remaining_amount = fields.Float('Remaining Amount', compute='_compute_remaining_amount', store=True,)
    # Dates
    date_created = fields.Date('Date Created', default=fields.Date.today, required=True)
    due_date = fields.Date('Payment Due Date')
    payment_date = fields.Date('Payment Date')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('waived', 'Waived'),
        ('cancelled', 'Cancelled')
    ], 'Status', default='draft', required=True, tracking=True)

    # Payment Information
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_banking', 'Mobile Banking'),
        ('adjustment', 'Adjustment')
    ], 'Payment Method')

    payment_reference = fields.Char('Payment Reference')
    collected_by = fields.Many2one('res.users', 'Collected By')

    # Waiver Information
    waived = fields.Boolean('Waived', tracking=True)
    waived_reason = fields.Text('Waived Reason')
    waived_by = fields.Many2one('res.users', 'Waived By')
    waived_date = fields.Date('Waived Date')

    # Description and Notes
    # description = fields.Text('Description', required=True)
    notes = fields.Text('Internal Notes')

    # Related Fields for easy access
    member_name = fields.Char(related='member_id.name', string='Member Name', readonly=True)
    book_name = fields.Char(related='book_id.name', string='Book Title', readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('library.book') or _('New')

        # Set due date if not provided (30 days from creation)
        if not vals.get('due_date'):
            vals['due_date'] = fields.Date.today() + timedelta(days=30)

        return super(LibraryFine, self).create(vals)

    @api.depends('amount', 'paid_amount')
    def _compute_remaining_amount(self):
        for fine in self:
            fine.remaining_amount = fine.amount - (fine.paid_amount or 0)

    @api.constrains('amount', 'paid_amount')
    def _check_amounts(self):
        for fine in self:
            if fine.amount < 0:
                raise ValidationError(_('Fine amount cannot be negative.'))
            if fine.paid_amount < 0:
                raise ValidationError(_('Paid amount cannot be negative.'))
            if fine.paid_amount > fine.amount:
                raise ValidationError(_('Paid amount cannot exceed fine amount.'))

    @api.constrains('payment_date', 'date_created')
    def _check_payment_date(self):
        for fine in self:
            if fine.payment_date and fine.date_created:
                if fine.payment_date < fine.date_created:
                    raise ValidationError(_('Payment date cannot be before fine creation date.'))

    def action_confirm_fine(self):
        """Confirm the fine"""
        for fine in self:
            if fine.state != 'draft':
                raise UserError(_('Only draft fines can be confirmed.'))

            fine.state = 'confirmed'
            fine.message_post(body=_('Fine has been confirmed.'))

    def action_collect_payment(self):
        """Open payment collection wizard"""
        self.ensure_one()
        if self.state not in ['confirmed', 'partial']:
            raise UserError(_('Payment can only be collected for confirmed or partially paid fines.'))

        return {
            'name': _('Collect Fine Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.fine.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_fine_id': self.id,
                'default_amount': self.remaining_amount,
                'default_payment_date': fields.Date.today(),
            }
        }

    def action_waive_fine(self):
        """Waive the fine"""
        self.ensure_one()
        if self.state in ['paid', 'waived', 'cancelled']:
            raise UserError(_('This fine cannot be waived.'))

        return {
            'name': _('Waive Fine'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.fine.waive.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_fine_id': self.id,
                'default_amount': self.remaining_amount,
            }
        }

    def register_payment(self, amount, payment_method, payment_reference=None):
        """Register payment for the fine"""
        self.ensure_one()

        if amount <= 0:
            raise ValidationError(_('Payment amount must be positive.'))

        if amount > self.remaining_amount:
            raise ValidationError(_('Payment amount cannot exceed remaining amount.'))

        # Update payment info
        self.paid_amount += amount
        self.payment_method = payment_method
        self.payment_reference = payment_reference
        self.payment_date = fields.Date.today()
        self.collected_by = self.env.user

        # Update state
        if self.remaining_amount <= 0:
            self.state = 'paid'
            message = _('Fine fully paid: %.2f BDT') % self.amount
        else:
            self.state = 'partial'
            message = _('Partial payment received: %.2f BDT (Remaining: %.2f BDT)') % (amount, self.remaining_amount)

        # Post message
        self.message_post(body=message)

    def action_cancel(self):
        """Cancel the fine"""
        for fine in self:
            if fine.state in ['paid', 'partial']:
                raise UserError(_('Paid or partially paid fines cannot be cancelled.'))

            fine.state = 'cancelled'
            fine.message_post(body=_('Fine has been cancelled.'))

    def name_get(self):
        result = []
        for fine in self:
            name = f"{fine.name} - {fine.member_id.name} ({fine.amount:.2f} BDT)"
            result.append((fine.id, name))
        return result

    @api.model
    def get_fine_statistics(self, domain=None):
        """Get fine statistics for dashboard"""
        if domain is None:
            domain = []

        fines = self.search(domain)

        return {
            'total_fines': len(fines),
            'total_amount': sum(fines.mapped('amount')),
            'paid_amount': sum(fines.mapped('paid_amount')),
            'pending_amount': sum(fines.mapped('remaining_amount')),
            'waived_fines': len(fines.filtered('waived')),
            'overdue_fines': len(fines.filtered(
                lambda f: f.due_date and f.due_date < fields.Date.today() and f.state in ['confirmed', 'partial'])),
        }
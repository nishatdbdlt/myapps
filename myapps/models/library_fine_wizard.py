# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LibraryFinePaymentWizard(models.TransientModel):
    _name = 'library.fine.payment.wizard'
    _description = 'Library Fine Payment Wizard'

    fine_id = fields.Many2one('library.fine', 'Fine', required=True)
    member_id = fields.Many2one(related='fine_id.member_id', string='Member', readonly=True)
    fine_amount = fields.Float(related='fine_id.amount', string='Fine Amount', readonly=True)
    paid_amount = fields.Float(related='fine_id.paid_amount', string='Already Paid', readonly=True)
    remaining_amount = fields.Float(related='fine_id.remaining_amount', string='Remaining Amount', readonly=True)

    # Payment fields
    amount = fields.Float('Payment Amount', required=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_banking', 'Mobile Banking'),
        ('adjustment', 'Adjustment')
    ], 'Payment Method', required=True, default='cash')

    payment_reference = fields.Char('Payment Reference')
    payment_date = fields.Date('Payment Date', default=fields.Date.today, required=True)
    notes = fields.Text('Notes')

    @api.constrains('amount')
    def _check_amount(self):
        for wizard in self:
            if wizard.amount <= 0:
                raise ValidationError(_('Payment amount must be positive.'))
            if wizard.amount > wizard.remaining_amount:
                raise ValidationError(
                    _('Payment amount cannot exceed remaining amount (%.2f BDT).') % wizard.remaining_amount)

    def action_collect_payment(self):
        """Process the payment"""
        self.ensure_one()

        if not self.fine_id:
            raise ValidationError(_('Fine record not found.'))

        # Register the payment
        self.fine_id.register_payment(
            amount=self.amount,
            payment_method=self.payment_method,
            payment_reference=self.payment_reference
        )

        # Add notes if provided
        if self.notes:
            self.fine_id.message_post(body=_('Payment Notes: %s') % self.notes)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class LibraryFineWaiveWizard(models.TransientModel):
    _name = 'library.fine.waive.wizard'
    _description = 'Library Fine Waive Wizard'

    fine_id = fields.Many2one('library.fine', 'Fine', required=True)
    member_id = fields.Many2one(related='fine_id.member_id', string='Member', readonly=True)
    fine_amount = fields.Float(related='fine_id.amount', string='Fine Amount', readonly=True)
    remaining_amount = fields.Float(related='fine_id.remaining_amount', string='Remaining Amount', readonly=True)

    # Waiver fields
    waive_reason = fields.Text('Waive Reason', required=True)
    waive_date = fields.Date('Waive Date', default=fields.Date.today, required=True)

    def action_waive_fine(self):
        """Process the fine waiver"""
        self.ensure_one()

        if not self.fine_id:
            raise ValidationError(_('Fine record not found.'))

        # Update fine record
        self.fine_id.write({
            'waived': True,
            'waived_reason': self.waive_reason,
            'waived_by': self.env.user.id,
            'waived_date': self.waive_date,
            'state': 'waived'
        })

        # Post message
        self.fine_id.message_post(
            body=_('Fine waived. Reason: %s') % self.waive_reason
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
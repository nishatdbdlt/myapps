# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class LibraryExtendWizard(models.TransientModel):
    _name = 'library.extend.wizard'
    _description = 'Library Extend Due Date Wizard'

    borrow_id = fields.Many2one('library.borrow', 'Borrow Record', required=True)
    book_id = fields.Many2one(related='borrow_id.book_id', string='Book', readonly=True)
    member_id = fields.Many2one(related='borrow_id.member_id', string='Member', readonly=True)
    current_due_date = fields.Date(related='borrow_id.due_date', string='Current Due Date', readonly=True)

    # Extension fields
    extension_days = fields.Integer('Extension Days', required=True, default=14)
    extension_reason = fields.Selection([
        ('academic', 'Academic Research'),
        ('illness', 'Member Illness'),
        ('technical', 'Technical Issues'),
        ('special', 'Special Permission'),
        ('other', 'Other Reason')
    ], 'Extension Reason', required=True, default='academic')

    custom_reason = fields.Text('Custom Reason',
                                help="Please specify the reason if 'Other Reason' is selected")
    new_due_date = fields.Date('New Due Date', compute='_compute_new_due_date', store=True)

    # Validation fields
    max_extensions_allowed = fields.Integer('Max Extensions Allowed', default=2)
    current_extensions = fields.Integer('Current Extensions', compute='_compute_current_extensions')
    can_extend = fields.Boolean('Can Extend', compute='_compute_can_extend')
    extension_message = fields.Text('Extension Message', compute='_compute_can_extend')

    @api.depends('current_due_date', 'extension_days')
    def _compute_new_due_date(self):
        for wizard in self:
            if wizard.current_due_date and wizard.extension_days:
                wizard.new_due_date = wizard.current_due_date + timedelta(days=wizard.extension_days)
            else:
                wizard.new_due_date = False

    @api.depends('borrow_id')
    def _compute_current_extensions(self):
        for wizard in self:
            if wizard.borrow_id:
                # Count existing extensions for this borrow record
                extensions = self.env['library.extension'].search_count([
                    ('borrow_id', '=', wizard.borrow_id.id)
                ])
                wizard.current_extensions = extensions
            else:
                wizard.current_extensions = 0

    @api.depends('current_extensions', 'max_extensions_allowed', 'member_id', 'borrow_id')
    def _compute_can_extend(self):
        for wizard in self:
            messages = []
            can_extend = True

            # Check maximum extensions limit
            if wizard.current_extensions >= wizard.max_extensions_allowed:
                can_extend = False
                messages.append(_('Maximum extensions limit (%d) reached.') % wizard.max_extensions_allowed)

            # Check if member can still borrow
            if wizard.member_id and not wizard.member_id.can_borrow:
                can_extend = False
                if wizard.member_id.blocked:
                    messages.append(_('Member is blocked.'))
                if wizard.member_id.unpaid_fines > 100:
                    messages.append(_('Member has outstanding fines.'))
                if wizard.member_id.expiry_date and wizard.member_id.expiry_date < fields.Date.today():
                    messages.append(_('Member membership has expired.'))

            # Check if book is reserved by someone else
            if wizard.book_id:
                reservations = self.env['library.reservation'].search([
                    ('book_id', '=', wizard.book_id.id),
                    ('state', '=', 'active'),
                    ('member_id', '!=', wizard.member_id.id)
                ])
                if reservations:
                    can_extend = False
                    messages.append(_('Book is reserved by another member.'))

            # Check if borrow is overdue for too long
            if wizard.borrow_id and wizard.borrow_id.overdue_days > 7:
                can_extend = False
                messages.append(_('Book is overdue for more than 7 days.'))

            wizard.can_extend = can_extend
            wizard.extension_message = '\n'.join(messages) if messages else _('Extension is allowed.')

    @api.constrains('extension_days')
    def _check_extension_days(self):
        for wizard in self:
            if wizard.extension_days <= 0:
                raise ValidationError(_('Extension days must be positive.'))
            if wizard.extension_days > 30:
                raise ValidationError(_('Extension cannot be more than 30 days.'))

    @api.constrains('extension_reason', 'custom_reason')
    def _check_custom_reason(self):
        for wizard in self:
            if wizard.extension_reason == 'other' and not wizard.custom_reason:
                raise ValidationError(_('Please provide a custom reason when selecting "Other Reason".'))

    def action_extend_due_date(self):
        """Process the due date extension"""
        self.ensure_one()

        if not self.can_extend:
            raise UserError(_('Cannot extend due date: %s') % self.extension_message)

        # Create extension record
        extension = self.env['library.extension'].create({
            'borrow_id': self.borrow_id.id,
            'book_id': self.book_id.id,
            'member_id': self.member_id.id,
            'old_due_date': self.current_due_date,
            'new_due_date': self.new_due_date,
            'extension_days': self.extension_days,
            'extension_reason': self.extension_reason,
            'custom_reason': self.custom_reason,
            'extended_by': self.env.user.id,
            'extension_date': fields.Date.today(),
        })

        # Update borrow record
        self.borrow_id.write({
            'due_date': self.new_due_date
        })

        # Post message to borrow record
        reason_text = dict(self._fields['extension_reason'].selection)[self.extension_reason]
        if self.extension_reason == 'other':
            reason_text += f": {self.custom_reason}"

        self.borrow_id.message_post(
            body=_('Due date extended by %d days. New due date: %s. Reason: %s') % (
                self.extension_days, self.new_due_date, reason_text
            )
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class LibraryExtension(models.Model):
    _name = 'library.extension'
    _description = 'Library Book Extension Record'
    _order = 'extension_date desc'

    name = fields.Char('Reference', readonly=True, default=lambda self: _('New'))
    borrow_id = fields.Many2one('library.borrow', 'Borrow Record', required=True, ondelete='cascade')
    book_id = fields.Many2one('library.book', 'Book', required=True)
    member_id = fields.Many2one('library.member', 'Member', required=True)

    # Date information
    old_due_date = fields.Date('Original Due Date', required=True)
    new_due_date = fields.Date('New Due Date', required=True)
    extension_date = fields.Date('Extension Date', default=fields.Date.today, required=True)
    extension_days = fields.Integer('Extension Days', required=True)

    # Reason and approval
    extension_reason = fields.Selection([
        ('academic', 'Academic Research'),
        ('illness', 'Member Illness'),
        ('technical', 'Technical Issues'),
        ('special', 'Special Permission'),
        ('other', 'Other Reason')
    ], 'Extension Reason', required=True)

    custom_reason = fields.Text('Custom Reason')
    extended_by = fields.Many2one('res.users', 'Extended By', required=True)

    # Related fields
    book_name = fields.Char(related='book_id.name', string='Book Title', readonly=True)
    member_name = fields.Char(related='member_id.name', string='Member Name', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('library.extension') or _('New')
        return super(LibraryExtension, self).create(vals)
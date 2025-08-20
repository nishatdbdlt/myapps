# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Book Borrowing'
    _order = 'borrow_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char('Reference', copy=False, readonly=True)
    book_id = fields.Many2one('library.book', 'Book', required=True, tracking=True)
    member_id = fields.Many2one('library.member', 'Member', required=True, tracking=True)

    # Dates
    borrow_date = fields.Date('Borrow Date', default=fields.Date.today, required=True, tracking=True)
    due_date = fields.Date('Due Date', required=True, tracking=True)
    actual_return_date = fields.Date('Actual Return Date', tracking=True)

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled')
    ], 'Status', default='draft', required=True, tracking=True)

    # Additional Information
    issued_by = fields.Many2one('res.users', 'Issued By', default=lambda self: self.env.user)
    returned_by = fields.Many2one('res.users', 'Returned By')
    notes = fields.Text('Notes')

    # Book Condition
    condition_on_borrow = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], 'Condition on Borrow', default='good')

    condition_on_return = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged')
    ], 'Condition on Return')

    # Rating and Review
    rating = fields.Selection([
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars')
    ], 'Rating')
    review = fields.Text('Review')

    # Computed Fields
    days_borrowed = fields.Integer('Days Borrowed', compute='_compute_days_borrowed', store=True)
    is_overdue = fields.Boolean('Is Overdue', compute='_compute_is_overdue')
    overdue_days = fields.Integer('Overdue Days', compute='_compute_overdue_days')
    fine_amount = fields.Float('Fine Amount', compute='_compute_fine_amount')

    # Related Fields for easy access
    book_name = fields.Char(related='book_id.name', string='Book Title', readonly=True)
    book_author = fields.Char(related='book_id.author_id.name', string='Author', readonly=True)
    book_isbn = fields.Char(related='book_id.isbn', string='ISBN', readonly=True)
    member_name = fields.Char(related='member_id.name', string='Member Name', readonly=True)
    member_type = fields.Selection(related='member_id.member_type', string='Member Type', readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('library.borrow') or _('New')

        # Set due date if not provided
        if not vals.get('due_date') and vals.get('member_id'):
            member = self.env['library.member'].browse(vals['member_id'])
            borrow_date = fields.Date.from_string(vals.get('borrow_date', fields.Date.today()))

            # Different loan periods based on member type
            if member.member_type == 'teacher':
                days = 30
            elif member.member_type == 'staff':
                days = 21
            elif member.member_type == 'vip':
                days = 45
            else:  # student, public
                days = 14

            vals['due_date'] = borrow_date + timedelta(days=days)

        return super(LibraryBorrow, self).create(vals)

    @api.depends('borrow_date', 'actual_return_date')
    def _compute_days_borrowed(self):
        for borrow in self:
            if borrow.borrow_date:
                end_date = borrow.actual_return_date or fields.Date.today()
                delta = fields.Date.from_string(end_date) - fields.Date.from_string(borrow.borrow_date)
                borrow.days_borrowed = delta.days
            else:
                borrow.days_borrowed = 0

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for borrow in self:
            borrow.is_overdue = (
                    borrow.state == 'borrowed' and
                    borrow.due_date and
                    borrow.due_date < today
            )

    @api.depends('due_date', 'actual_return_date', 'state')
    def _compute_overdue_days(self):
        for borrow in self:
            if borrow.due_date:
                if borrow.actual_return_date:
                    # Book returned, calculate overdue days if any
                    if borrow.actual_return_date > borrow.due_date:
                        delta = fields.Date.from_string(borrow.actual_return_date) - fields.Date.from_string(
                            borrow.due_date)
                        borrow.overdue_days = delta.days
                    else:
                        borrow.overdue_days = 0
                elif borrow.state == 'borrowed':
                    # Book not returned yet, calculate current overdue
                    today = fields.Date.today()
                    if today > borrow.due_date:
                        delta = today - fields.Date.from_string(borrow.due_date)
                        borrow.overdue_days = delta.days
                    else:
                        borrow.overdue_days = 0
                else:
                    borrow.overdue_days = 0
            else:
                borrow.overdue_days = 0

    @api.depends('overdue_days')
    def _compute_fine_amount(self):
        # Fine calculation: 2 BDT per day for overdue
        for borrow in self:
            if borrow.overdue_days > 0:
                borrow.fine_amount = borrow.overdue_days * 2.0
            else:
                borrow.fine_amount = 0.0

    @api.constrains('book_id', 'member_id', 'borrow_date')
    def _check_borrow_constraints(self):
        for borrow in self:
            if borrow.state == 'draft':
                continue

            # Check if book is available
            if borrow.book_id.state not in ['available', 'reserved']:
                raise ValidationError(_('Book "%s" is not available for borrowing.') % borrow.book_id.name)

            # Check if member can borrow
            if not borrow.member_id.can_borrow:
                reasons = []
                if not borrow.member_id.active:
                    reasons.append(_('Member is inactive'))
                if borrow.member_id.blocked:
                    reasons.append(_('Member is blocked'))
                if borrow.member_id.expiry_date and borrow.member_id.expiry_date < fields.Date.today():
                    reasons.append(_('Membership expired'))
                if borrow.member_id.current_borrowed >= borrow.member_id.max_books_allowed:
                    reasons.append(_('Borrowing limit exceeded'))
                if borrow.member_id.unpaid_fines > 100:
                    reasons.append(_('Outstanding fines exceed limit'))

                raise ValidationError(
                    _('Member "%s" cannot borrow books. Reasons: %s') %
                    (borrow.member_id.name, ', '.join(reasons))
                )

    @api.constrains('due_date', 'borrow_date')
    def _check_dates(self):
        for borrow in self:
            if borrow.due_date and borrow.borrow_date:
                if borrow.due_date < borrow.borrow_date:
                    raise ValidationError(_('Due date cannot be before borrow date.'))

    def action_confirm_borrow(self):
        """Confirm the borrowing"""
        for borrow in self:
            if borrow.state != 'draft':
                raise UserError(_('Only draft borrowing records can be confirmed.'))

            # Update book status
            borrow.book_id.state = 'borrowed'
            borrow.state = 'borrowed'

            # Post message
            borrow.message_post(
                body=_('Book "%s" has been borrowed by %s until %s') %
                     (borrow.book_id.name, borrow.member_id.name, borrow.due_date)
            )

    def action_return_book(self):
        """Return the book"""
        for borrow in self:
            if borrow.state != 'borrowed':
                raise UserError(_('Only borrowed books can be returned.'))

            # Open return wizard
            return {
                'name': _('Return Book'),
                'type': 'ir.actions.act_window',
                'res_model': 'library.return',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_book_id': borrow.book_id.id,
                    'default_member_id': borrow.member_id.id,
                    'default_borrow_id': borrow.id,
                    'default_return_date': fields.Date.today(),
                }
            }

    def action_mark_lost(self):
        """Mark book as lost"""
        for borrow in self:
            if borrow.state != 'borrowed':
                raise UserError(_('Only borrowed books can be marked as lost.'))

            borrow.state = 'lost'
            borrow.book_id.state = 'lost'
            borrow.actual_return_date = fields.Date.today()
            borrow.returned_by = self.env.user

            # Create fine for lost book
            self.env['library.fine'].create({
                'member_id': borrow.member_id.id,
                'book_id': borrow.book_id.id,
                'borrow_id': borrow.id,
                'fine_type': 'lost',
                'amount': borrow.book_id.price or 500.0,  # Default fine for lost book
                'description': _('Fine for lost book: %s') % borrow.book_id.name,
            })

            borrow.message_post(body=_('Book has been marked as lost.'))

    def action_extend_due_date(self):
        """Extend due date"""
        for borrow in self:
            if borrow.state != 'borrowed':
                raise UserError(_('Only borrowed books can have extended due dates.'))

            return {
                'name': _('Extend Due Date'),
                'type': 'ir.actions.act_window',
                'res_model': 'library.extend.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_borrow_id': borrow.id}
            }

    def action_cancel(self):
        """Cancel the borrowing"""
        for borrow in self:
            if borrow.state not in ['draft', 'borrowed']:
                raise UserError(_('Only draft or borrowed records can be cancelled.'))

            if borrow.state == 'borrowed':
                borrow.book_id.state = 'available'

            borrow.state = 'cancelled'
            borrow.message_post(body=_('Borrowing has been cancelled.'))

    @api.model
    def update_overdue_status(self):
        """Cron job to update overdue status"""
        today = fields.Date.today()
        overdue_borrows = self.search([
            ('state', '=', 'borrowed'),
            ('due_date', '<', today)
        ])

        if overdue_borrows:
            overdue_borrows.write({'state': 'overdue'})

            # Send notification emails
            for borrow in overdue_borrows:
                if borrow.member_id.email:
                    # Send overdue notification
                    pass  # Implementation for email notification

    def name_get(self):
        result = []
        for borrow in self:
            name = f"{borrow.name} - {borrow.book_id.name} ({borrow.member_id.name})"
            result.append((borrow.id, name))
        return result

    def action_view_book_details(self):
        self.ensure_one()
        return {
            'name': 'Book Details',
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'form',
            'res_id': self.book_id.id,
            'target': 'current',
        }

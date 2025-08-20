# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class LibraryReturn(models.Model):
    _name = 'library.return'
    _description = 'Library Book Return'
    _order = 'return_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char('Reference', copy=False, readonly=True)
    book_id = fields.Many2one('library.book', 'Book', required=True, tracking=True)
    member_id = fields.Many2one('library.member', 'Member', required=True, tracking=True)
    borrow_id = fields.Many2one('library.borrow', 'Borrow Record', required=True, tracking=True)

    # Dates
    return_date = fields.Date('Return Date', default=fields.Date.today, required=True, tracking=True)
    due_date = fields.Date(related='borrow_id.due_date', string='Due Date', readonly=True)
    borrow_date = fields.Date(related='borrow_id.borrow_date', string='Borrow Date', readonly=True)

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')
    ], 'Status', default='draft', required=True, tracking=True)

    # Return Information
    returned_by = fields.Many2one('res.users', 'Returned By', default=lambda self: self.env.user)
    condition_on_return = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged')
    ], 'Book Condition', required=True, default='good', tracking=True)

    # Late Return Information
    is_late = fields.Boolean('Late Return', compute='_compute_late_return', store=True)
    overdue_days = fields.Integer('Overdue Days', compute='_compute_overdue_days', store=True)
    fine_amount = fields.Float('Fine Amount', compute='_compute_fine_amount', store=True)
    fine_waived = fields.Boolean('Fine Waived', tracking=True)
    fine_waived_reason = fields.Text('Fine Waived Reason')
    fine_waived_by = fields.Many2one('res.users', 'Fine Waived By')

    # Damage Information
    damage_reported = fields.Boolean('Damage Reported', tracking=True)
    damage_description = fields.Text('Damage Description')
    damage_fine_amount = fields.Float('Damage Fine Amount')
    damage_photos = fields.Binary('Damage Photos')

    # Notes and Comments
    return_notes = fields.Text('Return Notes')
    internal_notes = fields.Text('Internal Notes')

    # Related Fields
    book_name = fields.Char(related='book_id.name', string='Book Title', readonly=True)
    book_author = fields.Char(related='book_id.author_id.name', string='Author', readonly=True)
    member_name = fields.Char(related='member_id.name', string='Member Name', readonly=True)

    # Fine Record
    fine_id = fields.Many2one('library.fine', 'Fine Record', readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('library.return') or _('New')
        return super(LibraryReturn, self).create(vals)

    @api.depends('return_date', 'due_date')
    def _compute_late_return(self):
        for return_rec in self:
            if return_rec.return_date and return_rec.due_date:
                return_rec.is_late = return_rec.return_date > return_rec.due_date
            else:
                return_rec.is_late = False

    @api.depends('return_date', 'due_date')
    def _compute_overdue_days(self):
        for return_rec in self:
            if return_rec.is_late and return_rec.return_date and return_rec.due_date:
                delta = fields.Date.from_string(return_rec.return_date) - fields.Date.from_string(return_rec.due_date)
                return_rec.overdue_days = delta.days
            else:
                return_rec.overdue_days = 0

    @api.depends('overdue_days', 'damage_fine_amount', 'fine_waived')
    def _compute_fine_amount(self):
        # Fine calculation: 2 BDT per day for overdue
        fine_per_day = 2.0

        for return_rec in self:
            total_fine = 0.0

            # Late return fine
            if return_rec.overdue_days > 0 and not return_rec.fine_waived:
                total_fine += return_rec.overdue_days * fine_per_day

            # Damage fine
            if return_rec.damage_reported and return_rec.damage_fine_amount:
                total_fine += return_rec.damage_fine_amount

            return_rec.fine_amount = total_fine

    @api.onchange('borrow_id')
    def _onchange_borrow_id(self):
        if self.borrow_id:
            self.book_id = self.borrow_id.book_id
            self.member_id = self.borrow_id.member_id

    @api.onchange('condition_on_return')
    def _onchange_condition_on_return(self):
        if self.condition_on_return == 'damaged':
            self.damage_reported = True
        else:
            self.damage_reported = False
            self.damage_description = False
            self.damage_fine_amount = 0.0

    @api.constrains('return_date', 'borrow_date')
    def _check_return_date(self):
        for return_rec in self:
            if return_rec.return_date and return_rec.borrow_date:
                if return_rec.return_date < return_rec.borrow_date:
                    raise ValidationError(_('Return date cannot be before borrow date.'))

    @api.constrains('damage_fine_amount')
    def _check_damage_fine_amount(self):
        for return_rec in self:
            if return_rec.damage_fine_amount < 0:
                raise ValidationError(_('Damage fine amount cannot be negative.'))

    def action_confirm_return(self):
        """Confirm the book return"""
        for return_rec in self:
            if return_rec.state != 'draft':
                raise UserError(_('Only draft returns can be confirmed.'))

            # Update borrow record
            return_rec.borrow_id.actual_return_date = return_rec.return_date
            return_rec.borrow_id.returned_by = return_rec.returned_by
            return_rec.borrow_id.condition_on_return = return_rec.condition_on_return
            return_rec.borrow_id.state = 'returned'

            # Update book status based on condition
            if return_rec.condition_on_return == 'damaged':
                return_rec.book_id.state = 'damaged'
            else:
                return_rec.book_id.state = 'available'

            # Create fine record if applicable
            if return_rec.fine_amount > 0:
                fine_description = []
                if return_rec.overdue_days > 0:
                    fine_description.append(_('%d days overdue') % return_rec.overdue_days)
                if return_rec.damage_reported:
                    fine_description.append(_('Book damage'))

                fine_id = self.env['library.fine'].create({
                    'member_id': return_rec.member_id.id,
                    'book_id': return_rec.book_id.id,
                    'borrow_id': return_rec.borrow_id.id,
                    'return_id': return_rec.id,
                    'fine_type': 'overdue' if return_rec.overdue_days > 0 else 'damage',
                    'amount': return_rec.fine_amount,
                    'description': _('Fine for: %s') % ', '.join(fine_description),
                    'waived': return_rec.fine_waived,
                    'waived_reason': return_rec.fine_waived_reason,
                    'waived_by': return_rec.fine_waived_by.id if return_rec.fine_waived_by else False,
                })
                return_rec.fine_id = fine_id

            # Update return status
            return_rec.state = 'returned'

            # Post message
            messages = [_('Book "%s" returned by %s') % (return_rec.book_id.name, return_rec.member_id.name)]
            if return_rec.is_late:
                messages.append(_('%d days late') % return_rec.overdue_days)
            if return_rec.fine_amount > 0:
                messages.append(_('Fine: %.2f BDT') % return_rec.fine_amount)
            if return_rec.damage_reported:
                messages.append(_('Damage reported'))

            return_rec.message_post(body=' - '.join(messages))

    def action_waive_fine(self):
        """Waive the fine"""
        for return_rec in self:
            if return_rec.state != 'draft':
                raise UserError(_('Fine can only be waived before confirming return.'))

            return {
                'name': _('Waive Fine'),
                'type': 'ir.actions.act_window',
                'res_model': 'library.fine.waive.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_return_id': return_rec.id,
                    'default_fine_amount': return_rec.fine_amount,
                }
            }

    def action_assess_damage(self):
        """Assess damage fine"""
        for return_rec in self:
            if not return_rec.damage_reported:
                raise UserError(_('No damage reported for this return.'))

            return {
                'name': _('Assess Damage Fine'),
                'type': 'ir.actions.act_window',
                'res_model': 'library.damage.assess.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_return_id': return_rec.id,
                    'default_book_id': return_rec.book_id.id,
                    'default_damage_description': return_rec.damage_description,
                }
            }

    def action_cancel(self):
        """Cancel the return"""
        for return_rec in self:
            if return_rec.state != 'draft':
                raise UserError(_('Only draft returns can be cancelled.'))

            return_rec.state = 'cancelled'
            return_rec.message_post(body=_('Return has been cancelled.'))

    def action_view_fine(self):
        """View related fine record"""
        self.ensure_one()
        if not self.fine_id:
            raise UserError(_('No fine record associated with this return.'))

        return {
            'name': _('Fine Record'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.fine',
            'res_id': self.fine_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def name_get(self):
        result = []
        for return_rec in self:
            name = f"{return_rec.name} - {return_rec.book_id.name} ({return_rec.member_id.name})"
            if return_rec.is_late:
                name += f" - {return_rec.overdue_days} days late"
            result.append((return_rec.id, name))
        return result

    @api.model
    def get_return_statistics(self, domain=None):
        """Get return statistics for dashboard"""
        if domain is None:
            domain = []

        returns = self.search(domain)

        stats = {
            'total_returns': len(returns),
            'on_time_returns': len(returns.filtered(lambda r: not r.is_late)),
            'late_returns': len(returns.filtered('is_late')),
            'damaged_returns': len(returns.filtered('damage_reported')),
            'total_fines': sum(returns.mapped('fine_amount')),
            'average_overdue_days': sum(returns.mapped('overdue_days')) / len(returns) if returns else 0,
        }

        stats['on_time_percentage'] = (stats['on_time_returns'] / stats['total_returns'] * 100) if stats[
            'total_returns'] else 0

        return stats
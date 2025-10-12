# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import re


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal Information
    name = fields.Char('Full Name', required=True, tracking=True)
    email = fields.Char('Email', tracking=True)
    phone = fields.Char('Phone Number', tracking=True)
    mobile = fields.Char('Mobile Number')
    date_of_birth = fields.Date('Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], 'Gender')

    # Address Information
    street = fields.Char('Street')
    street2 = fields.Char('Street 2')
    city = fields.Char('City')
    state = fields.Char('State')
    zip_code = fields.Char('ZIP Code')
    country_id = fields.Many2one('res.country', 'Country')

    # Member Details
    member_id = fields.Char('Member ID', copy=False, readonly=True)
    member_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('public', 'Public'),
        ('vip', 'VIP')
    ], 'Member Type', required=True, default='student', tracking=True)

    # Membership Status
    membership_date = fields.Date('Membership Date', default=fields.Date.today, tracking=True)
    expiry_date = fields.Date('Membership Expiry', tracking=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    blocked = fields.Boolean('Blocked', tracking=True)
    blocked_reason = fields.Text('Blocked Reason')

    # Contact Person (for students)
    guardian_name = fields.Char('Guardian Name')
    guardian_phone = fields.Char('Guardian Phone')
    emergency_contact = fields.Char('Emergency Contact')

    # Academic Information (for students/teachers)
    student_id = fields.Char('Student/Employee ID')
    department = fields.Char('Department')
    class_section = fields.Char('Class/Section')

    # Photo and Documents
    image = fields.Image('Photo', max_width=1920, max_height=1920)
    id_document = fields.Binary('ID Document')
    id_document_name = fields.Char('ID Document Name')

    # Library Statistics
    borrow_ids = fields.One2many('library.borrow', 'member_id', 'Borrowing History')
    return_ids = fields.One2many('library.return', 'member_id', 'Return History')
    fine_ids = fields.One2many('library.fine', 'member_id', 'Fines')


    # Computed Fields
    total_borrowed = fields.Integer('Total Books Borrowed', compute='_compute_library_stats')
    books_overdue = fields.Integer('Overdue Books', compute='_compute_library_stats')
    current_borrowed = fields.Integer('Currently Borrowed', compute='_compute_library_stats')
    total_fines = fields.Float('Total Fines', compute='_compute_fine_stats')
    unpaid_fines = fields.Float('Unpaid Fines', compute='_compute_fine_stats')

    # Borrowing Limits
    max_books_allowed = fields.Integer('Max Books Allowed', compute='_compute_borrowing_limits')
    can_borrow = fields.Boolean('Can Borrow', compute='_compute_can_borrow')

    # Notes
    notes = fields.Text('Notes')

    @api.model
    def create(self, vals):
        if not vals.get('member_id'):
            vals['member_id'] = self.env['ir.sequence'].next_by_code('library.member') or _('New')

        # Set default expiry date based on member type
        if not vals.get('expiry_date') and vals.get('member_type'):
            membership_date = fields.Date.from_string(vals.get('membership_date', fields.Date.today()))
            if vals['member_type'] == 'student':
                vals['expiry_date'] = membership_date + timedelta(days=365)  # 1 year
            elif vals['member_type'] in ['teacher', 'staff']:
                vals['expiry_date'] = membership_date + timedelta(days=1095)  # 3 years
            else:
                vals['expiry_date'] = membership_date + timedelta(days=730)  # 2 years

        return super(LibraryMember, self).create(vals)

    @api.depends('borrow_ids', 'borrow_ids.state', 'borrow_ids.due_date')
    def _compute_library_stats(self):
        for member in self:
            all_borrows = member.borrow_ids
            member.total_borrowed = len(all_borrows.filtered(lambda b: b.state != 'draft'))
            member.current_borrowed = len(all_borrows.filtered(lambda b: b.state == 'borrowed'))

            # Count overdue books
            overdue_borrows = all_borrows.filtered(
                lambda b: b.state == 'borrowed' and b.due_date and b.due_date < fields.Date.today()
            )
            member.books_overdue = len(overdue_borrows)

    @api.depends('fine_ids', 'fine_ids.amount', 'fine_ids.paid_amount')
    def _compute_fine_stats(self):
        for member in self:
            all_fines = member.fine_ids
            member.total_fines = sum(all_fines.mapped('amount'))
            member.unpaid_fines = sum(fine.amount - fine.paid_amount for fine in all_fines)

    @api.depends('member_type')
    def _compute_borrowing_limits(self):
        limits = {
            'student': 3,
            'teacher': 10,
            'staff': 5,
            'public': 2,
            'vip': 15
        }
        for member in self:
            member.max_books_allowed = limits.get(member.member_type, 3)

    @api.depends('blocked', 'active', 'expiry_date', 'current_borrowed', 'max_books_allowed', 'unpaid_fines')
    def _compute_can_borrow(self):
        for member in self:
            can_borrow = True

            # Check if member is active and not blocked
            if not member.active or member.blocked:
                can_borrow = False

            # Check membership expiry
            elif member.expiry_date and member.expiry_date < fields.Date.today():
                can_borrow = False

            # Check borrowing limit
            elif member.current_borrowed >= member.max_books_allowed:
                can_borrow = False

            # Check unpaid fines (assuming threshold of 100)
            elif member.unpaid_fines > 100:
                can_borrow = False

            member.can_borrow = can_borrow

    @api.constrains('email')
    def _check_email(self):
        for member in self:
            if member.email:
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', member.email):
                    raise ValidationError(_('Please enter a valid email address.'))

    @api.constrains('phone', 'mobile')
    def _check_phone(self):
        for member in self:
            for phone_field in [member.phone, member.mobile]:
                if phone_field:
                    # Remove spaces and special characters
                    cleaned_phone = re.sub(r'[^\d+]', '', phone_field)
                    if len(cleaned_phone) < 10:
                        raise ValidationError(_('Phone number must be at least 10 digits long.'))

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for member in self:
            if member.date_of_birth and member.date_of_birth > fields.Date.today():
                raise ValidationError(_('Date of birth cannot be in the future.'))

    @api.constrains('expiry_date')
    def _check_expiry_date(self):
        for member in self:
            if member.expiry_date and member.membership_date:
                if member.expiry_date < member.membership_date:
                    raise ValidationError(_('Expiry date cannot be before membership date.'))

    def action_renew_membership(self):
        """Renew membership for another period"""
        self.ensure_one()

        # Calculate new expiry date
        if self.member_type == 'student':
            new_expiry = fields.Date.today() + timedelta(days=365)
        elif self.member_type in ['teacher', 'staff']:
            new_expiry = fields.Date.today() + timedelta(days=1095)
        else:
            new_expiry = fields.Date.today() + timedelta(days=730)

        self.expiry_date = new_expiry
        self.message_post(body=_('Membership renewed until %s') % new_expiry)

    def action_block_member(self):
        """Block the member"""
        self.ensure_one()
        return {
            'name': _('Block Member'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.member.block.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_member_id': self.id}
        }

    def action_unblock_member(self):
        """Unblock the member"""
        self.ensure_one()
        self.blocked = False
        self.blocked_reason = False
        self.message_post(body=_('Member has been unblocked.'))

    def action_view_borrowed_books(self):
        """View currently borrowed books"""
        return {
            'name': _('Currently Borrowed Books'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id), ('state', '=', 'borrowed')],
            'context': {'default_member_id': self.id}
        }

    def action_view_borrow_history(self):
        """View complete borrowing history"""
        return {
            'name': _('Borrowing History'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id}
        }

    def action_view_fines(self):
        """View member's fines"""
        return {
            'name': _('Fines'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.fine',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id}
        }

    def name_get(self):
        result = []
        for member in self:
            name = f"[{member.member_id}] {member.name}"
            if member.member_type:
                name += f" ({dict(self._fields['member_type'].selection).get(member.member_type)})"
            result.append((member.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = [
                '|', '|', '|', '|',
                ('name', operator, name),
                ('member_id', operator, name),
                ('email', operator, name),
                ('phone', operator, name),
                ('student_id', operator, name)
            ]
            members = self.search(domain + args, limit=limit)
            return members.name_get()
        return self.search(args, limit=limit).name_get()

    def get_member_summary(self):
        """Get member summary for dashboard"""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'member_type': self.member_type,
            'current_borrowed': self.current_borrowed,
            'books_overdue': self.books_overdue,
            'unpaid_fines': self.unpaid_fines,
            'can_borrow': self.can_borrow,
            'expiry_date': self.expiry_date
        }
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char('Title', required=True, tracking=True)
    isbn = fields.Char('ISBN', size=13, tracking=True)
    author_id = fields.Many2one('library.author', 'Author', required=True, tracking=True)
    # publisher_id = fields.Many2one('library.publisher', 'Publisher')
    category_id = fields.Many2one('library.category', 'Category', required=True, tracking=True,ondelete='restrict')
    date_release=fields.Date(string='date_release')

    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    author_ids = fields.Many2many('library.author', string='Authors')

    # Book Details
    edition = fields.Char('Edition')
    pages = fields.Integer('Number of Pages')
    language = fields.Selection([
        ('bn', 'Bengali'),
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('ur', 'Urdu'),
        ('ar', 'Arabic'),
        ('other', 'Other')
    ], 'Language', default='bn')
    publication_date = fields.Date('Publication Date')
    price = fields.Float('Price', digits='Product Price')

    # Physical Details
    rack_location = fields.Char('Rack Location')
    barcode = fields.Char('Barcode', copy=False)
    book_cover = fields.Image('Book Cover', max_width=1920, max_height=1920)

    # Status and Availability
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
        ('maintenance', 'Under Maintenance')
    ], 'Status', default='available', required=True, tracking=True)

    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    notes = fields.Text('Internal Notes')

    # Related Records
    borrow_ids = fields.One2many('library.borrow', 'book_id', 'Borrowing History')
    return_ids = fields.One2many('library.return', 'book_id', 'Return History')

    current_borrower_id = fields.Many2one(
        'library.member', 'Current Borrower',
        compute='_compute_current_borrower', store=True)
    total_borrowed = fields.Integer('Times Borrowed', compute='_compute_borrow_stats')
    average_rating = fields.Float('Average Rating', compute='_compute_average_rating')

    # Auto-generated fields
    book_code = fields.Char('Book Code', copy=False, readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('book_code'):
            vals['book_code'] = self.env['ir.sequence'].next_by_code('library.book') or _('New')
        return super(LibraryBook, self).create(vals)

    @api.depends('borrow_ids', 'borrow_ids.state')
    def _compute_current_borrower(self):
        for book in self:
            current_borrow = book.borrow_ids.filtered(
                lambda b: b.state == 'borrowed' and not b.actual_return_date
            )
            book.current_borrower_id = current_borrow[:1].member_id.id if current_borrow else False

    @api.depends('borrow_ids')
    def _compute_borrow_stats(self):
        for book in self:
            book.total_borrowed = len(book.borrow_ids.filtered(lambda b: b.state != 'draft'))

    def _compute_average_rating(self):
        for book in self:
            ratings = book.borrow_ids.filtered('rating').mapped('rating')
            book.average_rating = sum(ratings) / len(ratings) if ratings else 0.0

    @api.constrains('isbn')
    def _check_isbn(self):
        for book in self:
            if book.isbn:
                # Remove hyphens and spaces
                isbn = re.sub(r'[-\s]', '', book.isbn)
                if len(isbn) not in [10, 13]:
                    raise ValidationError(_('ISBN must be 10 or 13 digits long.'))
                if not isbn.isdigit():
                    raise ValidationError(_('ISBN must contain only digits.'))

    @api.constrains('pages')
    def _check_pages(self):
        for book in self:
            if book.pages and book.pages < 1:
                raise ValidationError(_('Number of pages must be positive.'))

    @api.constrains('publication_date')
    def _check_publication_date(self):
        for book in self:
            if book.publication_date and book.publication_date > fields.Date.today():
                raise ValidationError(_('Publication date cannot be in the future.'))

    def action_borrow_book(self):
        """Open borrow wizard for this book"""
        return {
            'name': _('Borrow Book'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_id': self.id,
                'default_borrow_date': fields.Date.today(),
            }
        }

    def action_return_book(self):
        """Open return wizard for this book"""
        current_borrow = self.borrow_ids.filtered(
            lambda b: b.state == 'borrowed' and not b.actual_return_date
        )
        if not current_borrow:
            raise ValidationError(_('This book is not currently borrowed.'))

        return {
            'name': _('Return Book'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.return',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_id': self.id,
                'default_borrow_id': current_borrow[0].id,
                'default_return_date': fields.Date.today(),
            }
        }

    def action_reserve_book(self):
        """Reserve the book"""
        self.ensure_one()
        if self.state != 'available':
            raise ValidationError(_('Only available books can be reserved.'))

        self.state = 'reserved'
        self.message_post(body=_('Book has been reserved.'))

    def action_make_available(self):
        """Make the book available"""
        self.ensure_one()
        self.state = 'available'
        self.message_post(body=_('Book is now available.'))

    def action_mark_damaged(self):
        """Mark book as damaged"""
        self.ensure_one()
        self.state = 'damaged'
        self.message_post(body=_('Book has been marked as damaged.'))

    def action_mark_lost(self):
        """Mark book as lost"""
        self.ensure_one()
        self.state = 'lost'
        self.message_post(body=_('Book has been marked as lost.'))

    def name_get(self):
        result = []
        for book in self:
            name = f"[{book.book_code}] {book.name}"
            if book.author_id:
                name += f" - {book.author_id.name}"
            result.append((book.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = [
                '|', '|', '|', '|',
                ('name', operator, name),
                ('book_code', operator, name),
                ('isbn', operator, name),
                ('author_id.name', operator, name),
                ('barcode', operator, name)
            ]
            books = self.search(domain + args, limit=limit)
            return books.name_get()
        return self.search(args, limit=limit).name_get()

    def _get_availability_status(self):
        """Get human readable availability status"""
        status_map = {
            'available': _('Available'),
            'borrowed': _('Borrowed'),
            'reserved': _('Reserved'),
            'damaged': _('Damaged'),
            'lost': _('Lost'),
            'maintenance': _('Under Maintenance')
        }
        return status_map.get(self.state, self.state)

    def action_view_borrow_history(self):
        self.ensure_one()
        return {
            'name': 'Borrow History',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'view_mode': 'tree,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id},
        }

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = "Book Author"
    _order = 'name'

    name = fields.Char('Author Name', required=True)
    biography = fields.Text('Biography')
    birth_day = fields.Date('Birth Day')
    death_date = fields.Date('Death Date')
    nationality = fields.Char('Nationality')
    email = fields.Char('Email')
    website = fields.Char('Website')
    image = fields.Image('Photo', max_width=1920, max_height=1920)
    active = fields.Boolean('Active', default=True)
    books_ids = fields.One2many('library.book', 'author_id', string='Books')
    # book_id=fields.Char('book_id')
    book_count = fields.Integer('Number of Books', compute='_compute_book_count')

    @api.depends('books_ids')
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.books_ids)

    @api.constrains('birth_day', 'death_date')
    def _check_dates(self):
        for author in self:
            if author.birth_day and author.death_date:
                if author.birth_day > author.death_date:
                    raise ValidationError(_('Birth date cannot be later than death date.'))

    def action_view_books(self):
        return {
            'name': _('Books by %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
             'domain': [('author_id', '=', self)],
             'context': {'default_author_id': self},
        }

    def name_get(self):
        result = []
        for author in self:
            name = author.name
            if author.nationality:
                name = f"{name} ({author.nationality})"
            result.append((author.id, name))
        return result

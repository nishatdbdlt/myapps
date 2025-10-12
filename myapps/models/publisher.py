# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Book Publisher'
    _order = 'name'

    name = fields.Char('Publisher Name', required=True)
    description = fields.Text('Description')

    # Contact Information
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    website = fields.Char('Website')

    # Address
    street = fields.Char('Street')
    street2 = fields.Char('Street 2')
    city = fields.Char('City')
    state = fields.Char('State')
    zip_code = fields.Char('ZIP Code')
    country_id = fields.Many2one('res.country', 'Country')

    # Additional Information
    founded_year = fields.Integer('Founded Year')
    logo = fields.Image('Logo', max_width=1920, max_height=1920)
    active = fields.Boolean('Active', default=True)

    # Relations
    book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    book_count = fields.Integer('Number of Books', compute='_compute_book_count')

    @api.depends('book_ids')
    def _compute_book_count(self):
        for publisher in self:
            publisher.book_count = len(publisher.book_ids)

    @api.constrains('founded_year')
    def _check_founded_year(self):
        current_year = fields.Date.today().year
        for publisher in self:
            if publisher.founded_year and (publisher.founded_year < 1000 or publisher.founded_year > current_year):
                raise ValidationError(_('Founded year must be between 1000 and %d.') % current_year)

    def action_view_books(self):
        """Open books view filtered by this publisher"""
        return {
            'name': _('Books by %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
            'domain': [('publisher_id', '=', self.id)],
            'context': {'default_publisher_id': self.id},
        }

    def name_get(self):
        result = []
        for publisher in self:
            name = publisher.name
            if publisher.city:
                name = f"{publisher.name} ({publisher.city})"
            result.append((publisher.id, name))
        return result
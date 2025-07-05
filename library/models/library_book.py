from odoo import models, fields, api


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Name', required=True)
    author = fields.Char(string='Author')
    price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity')

    issued_book_ids = fields.One2many('library.issue', 'book_id', string='Issued Books')

    # Correct compute methods assigned
    issued_book_count = fields.Integer(string='Issued Book', compute='_compute_issued_book_count')
    issued_count = fields.Integer(string="Issued Count", compute="_compute_issued_count")

    rack_no = fields.Integer(string='Rack No')
    status = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ], string='Status', default='available')

    @api.depends('issued_book_ids')
    def _compute_issued_book_count(self):
        for record in self:
            record.issued_book_count = len(record.issued_book_ids or [])

    def _compute_issued_count(self):
        for record in self:
            record.issued_count = self.env['library.issue'].search_count([('book_id', '=', record.id)])

    # @api.depends('book_id', 'book_id.issued_book_ids')
    # def _compute_issued_book_count(self):
    #     for rec in self:
    #         if not rec.book_id:
    #             rec.serial_no = 0
    #             continue
    #
    #         # Get all related issues of this book (in memory-safe way)
    #         related_issues = rec.book_id.issued_book_ids.sorted('create_date')
    #
    #         # Fallback if create_date is not available (for unsaved lines)
    #         if any(not issue.create_date for issue in related_issues):
    #             related_issues = sorted(
    #                 rec.book_id.issued_book_ids,
    #                 key=lambda x: x.id or 0  # sort by ID if create_date is not set
    #             )
    #
    #         # Recalculate serial number based on position
    #         for index, issue in enumerate(related_issues, start=1):
    #             if issue == rec:
    #                 rec.serial_no = index
    #                 break

    # def action_view_issued_students(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Issued Students',
    #         'view_mode': 'tree,form',
    #         'res_model': 'library.issue',
    #         'domain': [('book_id', '=', self.id)],
    #         'context': {'default_book_id': self.id},
    #         'target': 'new',
    #     }
    #


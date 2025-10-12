from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryCategory(models.Model):
    _name = "library.category"
    _description = "Library Book Category"
    _order = "name"
    _parent_store = True
    _parent_name = "parent_id"
    _rec_name = "complete_name"

    name = fields.Char('Category Name', required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)
    parent_id = fields.Many2one('library.category', string='Parent Category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)

    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Color Index')

    book_count = fields.Integer('Number of Books', compute='_compute_book_count')

    child_id = fields.One2many('library.category', 'parent_id', string='Child Categories')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.depends('child_id')
    def _compute_book_count(self):
        for category in self:
            category.book_count = self.env['library.book'].search_count([('category_id', 'child_of', category.id)])

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    def name_get(self):
        result = []
        for category in self:
            name = category.complete_name or category.name
            result.append((category.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = ['|', ('name', operator, name), ('complete_name', operator, name)]
            categories = self.search(domain + args, limit=limit)
            return categories.name_get()
        return self.search(args, limit=limit).name_get()

    def action_view_book(self):
        return {
            'name': _('Books in category: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
            'domain': [('category_id', 'child_of', self.id)],
            'context': {"default_category_id": self.id}
        }

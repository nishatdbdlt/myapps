# from odoo import models, fields
#
# from odoo import models, fields
#
# class LibraryIssue(models.Model):
#     _name = 'library.book.issue'
#     _description = 'Library Book Issue'
#
#     user_type = fields.Selection([
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#         ('staff', 'Staff'),
#     ], string='User Type', required=True)
#     user_id = fields.Many2one('library.user', string='User', required=True)
#     library_id = fields.Char(related='user_id.library_id', string='Library ID', store=True)
#     book_id = fields.Many2one('library.book', string='Book', required=True)
#     subject_code = fields.Char(related='book_id.subject_code', string='Subject Code', store=True)
#     author = fields.Char(related='book_id.author', string='Author', store=True)
#     # Inside your Python model (optional)
#     book_name = fields.Char(related='book_id.name', string='Book Name', store=True)
#     student_class = fields.Char(related='user_id.student_class', string='Class', store=True)
#     section = fields.Char(related='user_id.section', string='Section', store=True)
#     student_name = fields.Char(related='user_id.student_name', string='Student Name', store=True)
#
#     due_date = fields.Date('Due Date')
#     note = fields.Text('Note')
#
#     class LibraryUser(models.Model):
#         _name = 'library.user'
#         _description = 'Library User'
#
#         name = fields.Char('Full Name', required=True)
#         user_type = fields.Selection([
#             ('student', 'Student'),
#             ('teacher', 'Teacher'),
#             ('staff', 'Staff'),
#         ], string='User Type', required=True)
#         library_id = fields.Char('Library ID', required=True)
#         class_name = fields.Char('Class')
#         section = fields.Char('Section')
#         student_class = fields.Char(string='Class')  # <-- add this
#         student_name = fields.Char(string='Student Name')  # <-- add
#         user_id=fields.Char(string='user_id')
#         # other fields...
#
#
#
#
#

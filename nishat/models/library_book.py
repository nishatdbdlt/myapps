from odoo import models, fields ,api
from odoo.tools.populate import compute


class LibraryIssue(models.Model):
    _name = 'library.issue'
    _description = 'Issued Book'

    student_id = fields.Many2one('school.student',string='Student Name')
    # student=fields.Char(string='student')
    student_class_id = fields.Many2one('school.class', string='Class')  # ✅ FIXED    roll_number = fields.Char(string='Roll')
    # student_class = fields.Integer(string='class')
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today)
    book_id = fields.Many2one('library.book', string='Book')
    serial_no = fields.Integer(string='Serial No', compute='_compute_serial_no', store=False)
    roll=fields.Integer(string='roll')
    user_id = fields.Many2one('res.users', string="Issued By", default=lambda self: self.env.user)
    @api.depends('book_id')
    def _compute_serial_no(self):
        # Group records by book to optimize DB queries
        issues_by_book = {}
        for record in self:
            record.serial_no = 0  # default value
            if record.book_id:
                issues_by_book.setdefault(record.book_id.id, []).append(record)

        for book_id, records in issues_by_book.items():
            # Get all issues for this book ordered by create_date
            all_issues = self.env['library.issue'].search(
                [('book_id', '=', book_id)],
                order='create_date'
            )

            # Map each issue's ID to its serial number
            issue_id_to_serial = {issue.id: idx + 1 for idx, issue in enumerate(all_issues)}

            for record in records:
                # Set serial number only if the record is saved (has ID)
                if record.id in issue_id_to_serial:
                    record.serial_no = issue_id_to_serial[record.id]


    def print_all_reports(self):
        all_ids = self.search([]).ids
        return self.env.ref('nishat.report_library_issue_tamplate').report_action(all_ids)
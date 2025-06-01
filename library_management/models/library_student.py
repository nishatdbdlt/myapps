from odoo import models, fields

class LibraryStudent(models.Model):
    _name = 'library.student'
    _description = 'Library Student'

    name = fields.Char(string="Name", required=True)
    photo = fields.Image(string="Photo")
    roll = fields.Char(string="Roll")
    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')], string="User Type", required=True)
    class_id = fields.Many2one('school.class', string="Class")
    section = fields.Selection([
        ('গোলাপ', 'Section গোলাপ'),
        ('শাপলা', 'Section শাপলা'),
        ('বেলি', 'Section বেলি'),
    ], string="Section")
    phone = fields.Char(string="Phone")

    def action_make_member(self):
        # Perform the action, e.g., creating a member record
        for student in self:
            # Your logic here
            pass
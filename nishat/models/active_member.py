# from odoo import models, fields, api
#
# class EduActiveMember(models.Model):
#     _name = 'edu.active.member'
#     _description = 'Active Member in Education System'
#     _rec_name = 'user_type'
#
#     user_type = fields.Selection([
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#     ], string="User Type", required=True)
#
#     select_class = fields.Many2one('school.class', string="Class")
#
#     selected_section = fields.Selection([
#         ('all', 'All Students'),
#         ('golap', 'গোলাপ'),
#         ('shapla', 'শাপলা'),
#         # Add more if needed
#     ], string="Select Section", default='all')
#
#     student_ids = fields.Many2many(
#         'school.student',
#         string="Students",
#         compute='_compute_student_ids',
#         store=False,
#     )
#
#     # @api.depends('user_type', 'select_class', 'selected_section')
#     # def _compute_student_ids(self):
#     #     section_map = {
#     #         'golap': 'গোলাপ',
#     #         'shapla': 'শাপলা',
#     #     }
#     #
#     #     for rec in self:
#     #         if rec.user_type != 'student' or not rec.select_class:
#     #             rec.student_ids = self.env['school.student'].browse([])
#     #             continue
#     #
#     #         domain = [('class_id', '=', rec.select_class.id)]
#     #
#     #         if rec.selected_section and rec.selected_section != 'all':
#     #             real_section_name = section_map.get(rec.selected_section)
#     #             if real_section_name:
#     #                 domain.append(('section_id.name', '=', real_section_name))
#     #
#     #         rec.student_ids = self.env['school.student'].search(domain)
#
from odoo import models, fields, api



class EduActiveMember(models.Model):
    _name = 'edu.active.member'
    _description = 'Active Member in Education System'
    _rec_name='user_type'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    # select_class_id = fields.Many2one('school.class', string="Class") todo for connection
    select_id=fields.Char(string='Class')

    # student_ids = fields.Many2many(
    #     'school.student',
    #     string="Students",
    #     compute='_compute_student_ids',
    #     store=False
    # ) todo  for connection

    students=fields.Char(string="Students")

    # @api.depends('user_type', 'select_class_id')
    # def _compute_student_ids(self):
    #     for rec in self:
    #         if rec.user_type == 'student' and rec.select_class_id:
    #             students = self.env['school.student'].search([('class_id', '=', rec.select_class_id.id)])
    #             rec.student_ids = students
    #         else:
    #             rec.student_ids = False
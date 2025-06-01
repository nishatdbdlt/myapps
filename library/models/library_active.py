from odoo import models, fields, api

class LibraryActiveMember(models.TransientModel):
    _name = 'library.active.member'
    _description = 'Library Active Member Filter'

    user_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], string="User Type", required=True)

    select_class_id = fields.Many2one('school.class', string="Class", required=True)
    section_id = fields.Many2one('school.section', string="Section")

    # dynamically limit sections to those in the selected class
    @api.onchange('select_class_id')
    def _onchange_select_class_id(self):
        if self.select_class_id:
            return {'domain': {'section_id': [('class_id', '=', self.select_class_id.id)]}}
        else:
            return {'domain': {'section_id': []}}

    def action_show_students_by_section(self):
        self.ensure_one()
        if not self.section_id:
            # fallback: maybe show all students in class and user_type if no section selected
            domain = [
                ('user_type', '=', self.user_type),
                ('class_id', '=', self.select_class_id.id),
            ]
        else:
            domain = [
                ('user_type', '=', self.user_type),
                ('class_id', '=', self.select_class_id.id),
                ('section_id', '=', self.section_id.id),
            ]
        return {
            'name': 'Students',
            'type': 'ir.actions.act_window',
            'res_model': 'school.student',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

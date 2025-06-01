from odoo import models, fields, api

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string="Class Name", required=True)
    section_ids = fields.One2many('school.section', 'class_id', string="Sections")

class SchoolSection(models.Model):
    _name = 'school.section'
    _description = 'School Section'

    name = fields.Char(string="Section Name", required=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)

    def action_view_students(self):
        self.ensure_one()
        return {
            'name': f'Students in Section {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'school.student',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [
                ('class_id', '=', self.class_id.id),
                ('section_id', '=', self.id),
                ('user_type', '=', self.env.context.get('default_user_type')),
            ],
        }




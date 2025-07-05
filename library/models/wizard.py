from odoo import models, fields

class LibraryMemberWizard(models.TransientModel):
    _name = 'library.member.wizard'
    _description = 'Library Member Wizard'

    student_id = fields.Many2one('edu.member', string="Student", readonly=True)
    library_id = fields.Integer(string="Library ID")
    temp_library_id = fields.Char(string="Temporary Library ID")
    library_fee = fields.Float(string="Library Fee")

    def action_save_member(self):
        self.ensure_one()
        self.student_id.write({
            'library_id': self.library_id,
            'temp_library_id': self.temp_library_id,
            'library_fee': self.library_fee,
        })
        return {'type': 'ir.actions.act_window_close'}

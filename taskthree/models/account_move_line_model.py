from odoo import  models,fields,api

class account_move_line_model(models.Model):
    _inherit = 'account.move.line'

    dimension = fields.Char(string='Dimension')



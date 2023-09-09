from odoo import  models,fields,api

class stock_move_model(models.Model):
    _inherit = 'stock.move'
    dimension= fields.Char(string='Dimension')


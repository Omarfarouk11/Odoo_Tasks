from odoo import  models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            for move in line.move_ids:
                move.dimension = line.dimension
        return res






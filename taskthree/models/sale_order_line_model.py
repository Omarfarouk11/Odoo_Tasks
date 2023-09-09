from odoo import  models,fields,api

class sale_order_line_model(models.Model):
    _inherit = 'sale.order.line'
    dimension= fields.Char(string='Dimension')

    def _prepare_invoice_line(self, **optional_values):
        res = super(sale_order_line_model, self)._prepare_invoice_line()
        res.update({
            'dimension': self.move_ids.dimension
        })
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.product_tmpl_id.dimension:
            self.dimension = self.product_id.product_tmpl_id.dimension
        else:
            self.dimension = False


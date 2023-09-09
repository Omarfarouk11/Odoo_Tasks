from odoo import models, fields, api
from odoo.exceptions import ValidationError
class inherent_purchase_order_model(models.Model):
    _inherit = "purchase.order"
    purchase_id = fields.Many2one("purchase_requests", string="Request")
    def button_confirm(self):
        for order in self:
            if order.purchase_id:
                for line in order.order_line:
                    confirmed_po = self.env['purchase.order'].search([('purchase_id', '=', order.purchase_id.id), ('state', '=', 'purchase')])

                    confirmed_qty = 0
                    for po in confirmed_po:
                        confirmed_qty += po.order_line.filtered(
                            lambda x: x.product_id == line.order_id.product_id.id).product_qty

                    requestline = order.purchase_id.order_id.filtered(
                        lambda x: x.product_id == line.product_id)
                    request_qty = requestline.Quantity
                    qty = confirmed_qty + line.product_qty
                    if qty > request_qty:
                        raise ValidationError('Request Quantity is less Than the Product Quantity')

        res = super(inherent_purchase_order_model, self).button_confirm()

        return res

class inherent_purchase_order_line_model(models.Model):
    _inherit = "purchase.order.line"
    purchase_id = fields.Many2one("purchase_requests", string="Request")



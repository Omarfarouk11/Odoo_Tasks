from odoo import models, fields, api


class Order(models.Model):
    _name = "create_order"
    _description = "TaskOne"

    Purchase_ids = fields.Many2one("purchase_requests", string="Purchases")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    Description = fields.Char(string='Description', related="product_id.name")
    Quantity = fields.Float(default=1, string="Quantity")
    Cost_Price = fields.Float(string="Cost Price", related="product_id.standard_price")
    Total = fields.Float(string="Total", compute="_calculate_total")
    Requested_quantity = fields.Float(string="Requested_Quantity",default=1)
    Reminder_quantity = fields.Float(string="Reminder_Quantity",default=1)



    @api.depends("Cost_Price", "Quantity")
    def _calculate_total(self):
        for rec in self:
            if rec.Total == 0:
                rec.Total = rec.Quantity * rec.Cost_Price
            else:
                rec.Total = 0

    # def create_po(self):
    #
    #     for record in self:
    #
    #         if record.Purchase_ids:
    #             purchase_order = self.env["purchase.order"].browse(record.Purchase_ids.Purchase_order_id)
    #             order_id = record.Purchase_ids.order_id
    #             purchase_order_lines = []
    #             purchase_order_lines.append((0, 0, {
    #                     'product_id':record.product_id.id,
    #                     'name': record.product_id.name,
    #                     'product_qty': record.Quantity,
    #                     'price_unit': record.Total,
    #                     'order_id': order_id
    #                 }))
    #             activeid=purchase_order.id































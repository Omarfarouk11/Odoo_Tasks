from odoo import  models,fields, api
from _datetime import  date

from odoo.exceptions import *


class Purchase(models.Model):
    _name = "purchase_requests"
    _description = "TaskOne"
    requestname=fields.Char(string="Requestname",required=True)
    requested_id=fields.Many2one("res.users",required=True,string="Users",default=lambda self: self.env.user)
    start_date=fields.Date(string="StartDate",default=date.today())
    end_date=fields.Datetime(string="EndDate")
    order_id = fields.One2many("create_order","Purchase_ids",string="Order")
    Total_id=fields.Float(related="order_id.Total")
    Total_Price=fields.Float(string="Total Price",compute="_compute_total_price")
    state=fields.Selection([('draft',"Draft"),("to_be_approved","To Be Approved"),("approve","Approve"),("reject","Reject"),("cancel","Cancel")],default="draft",string="status")
    Rejection_reason=fields.Text(string="Rejection_Reason")
    purchase_id=fields.One2many("purchase.order","purchase_id",string="purchase_order")
    Purchase_order_line_id=fields.One2many("purchase.order.line","purchase_id",string="purchase_order_line")


    @api.depends("Total_id")
    def _compute_total_price(self):
        for rec in self:
            if rec.Total_id:
                rec.Total_Price=sum(rec.Total for rec in rec.order_id)
            else:
                rec.Total_Price=0

    def submit_for_approval(self):
        self.write({'state': 'to_be_approved'})

    def cancel(self):
        self.write({'state': 'cancel'})


    def resettodraft(self):
        self.write({"state":"draft"})

    def approve(self):
        self.write({"state":"approve"})
        self.send_approval_email()
    def send_approval_email(self):

        if self.state in ['approve']:
            purchase_managers = self.env.ref('taskone.group_purchase').users
            if purchase_managers:
                email_subject = f"Purchase Request ({self.requestname}) has been approved"
                email_body = f"Dear Purchase Manager,\n\nThe purchase request ({self.requestname}) has been approved."
                for manager in purchase_managers:
                    email_values = {
                        'auto_delete': True,
                        'subject': email_subject,
                        'author_id': self.env.user.id,
                        'body_html': email_body,
                        'email_to': manager.partner_id.email_formatted,
                        'email_from': self.env.user.partner_id.email_formatted
                    }
                    self.env['mail.mail'].create(email_values).send()



    def create_po(self):
        PurchaseOrder = self.env['purchase.order']
        for record in self:
            purchase_order_lines = []
            for order_line in record.order_id:
                purchase_order_lines.append((0, 0, {
                    'product_id':order_line.product_id.id,
                    'name': order_line.product_id.name,
                    'product_qty': order_line.Quantity,
                    'price_unit': order_line.Total,
                    'order_id': record.order_id,
                    'purchase_id':record.id
                }))
            purchase_order = PurchaseOrder.create({
                'partner_id':record.requested_id.partner_id.id ,
                'name': record.requestname,
                'order_line': purchase_order_lines,
                'company_id': self.env.company.id,
                'currency_id': self.env.company.currency_id.id,
                'date_order':record.end_date,
                'purchase_id': record.id
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'PO',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,

        }



    #
    #
    # def create_po(self):
    #     orders_line = []
    #     for record in self:
    #         for order in self.order_id:
    #             orders_line.append((0, 0,
    #                                 {   'product_id': order.product_id.id,
    #                                     'name': order.product_id.name,
    #                                     'product_qty': order.Quantity,
    #                                     'price_unit': order.Total,
    #                                     'order_id': record.order_id,
    #                                  }
    #
    #                                 ))
    #
    #     purchase_order = self.env['purchase.order'].create(
    #         {
    #             'partner_id': self.purchase_id.partner_id.id,
    #             'order_line': orders_line,
    #             'name': self.requestname,
    #             'company_id': self.env.company.id,
    #             'currency_id': self.env.company.currency_id.id,
    #             'date_order':self.end_date
    #         }
    #     )
    #
    #     return {
    #         'name': 'Create purchase.order',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'purchase.order',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_id': purchase_order.id,
    #
    #     }

    # def create_po(self):
    #
    #     purchase_order_lines = []
    #     for record in self:
    #         for order in record.order_id:
    #             purchase_order_lines.append((0, 0, {
    #                 'product_id': order.product_id.id,
    #                 'name': order.product_id.name,
    #                 'product_qty': order.Quantity,
    #                 'price_unit': order.Total,
    #                 'order_id': record.order_id,
    #
    #             }))
    #
    #         PurchaseOrder = self.env['purchase.order'].browse(record.id)
    #         if PurchaseOrder:
    #             PurchaseOrder.write({
    #                 'order_line': purchase_order_lines,
    #                  'purchase_id':record.id
    #             })
    #         else:
    #          PurchaseOrder.create({
    #                         'partner_id': record.requested_id.partner_id.id,
    #                         'name': record.requestname,
    #                         'order_line': purchase_order_lines,
    #                         'company_id': self.env.company.id,
    #                         'currency_id': self.env.company.currency_id.id,
    #                         'date_order':record.end_date,
    #                         'purchase_id': record.id
    #             })
    #
    #     return {
    #                 'name': 'PO',
    #                 'type': 'ir.actions.act_window',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'res_model': 'purchase.order',
    #                 'res_id': PurchaseOrder.id,
    #             }

    # def create_po(self):
    #     context = {}
    #     for record in self:
    #         context["pname"] = record.pname
    #         purchase_order = self.env["purchase.order"].with_context(context)
    #         for order in record.order_id:
    #                 purchase_order_lines = []
    #                 purchase_order_lines.append((0, 0, {
    #                     'product_id': order.product_id.id,
    #                     'name': order.product_id.name,
    #                     'product_qty': order.Quantity,
    #                     'price_unit': order.Total,
    #                     'order_id': record.order_id
    #                 }))


    #
    #
    #


            # for line in purchase_order.order_line:
    #     if line.product_qty > record.order_id.Quantity:
    #         line.product_qty = record.order_id.Quantity
    #


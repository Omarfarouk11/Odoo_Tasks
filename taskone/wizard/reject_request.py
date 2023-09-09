from odoo import api,models,fields


class Reject_wizard(models.TransientModel):
       _name="reject_wizard"
       _description = "Reject Wizard"
       purchase_id = fields.Many2one("purchase_requests", string="Purchase Request")
       Rejection = fields.Text(string="Rejection Reason")

       def Cancel_Wizard(self):
              return {'type': 'ir.actions.act_window_close'}

       def Confirm_Wizard(self):
              self.ensure_one()
              active_id = self.env.context.get('active_id')
              purchase = self.env['purchase_requests'].browse(active_id)
              purchase.write({'state': 'reject',
                              'Rejection_reason': self.Rejection})
              return {'type': 'ir.actions.act_window_close'}





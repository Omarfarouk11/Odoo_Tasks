from odoo import  models,fields,api

class producttemplatemodel(models.Model):
    _inherit = "product.template"
    dimension = fields.Char(string="Dimension")




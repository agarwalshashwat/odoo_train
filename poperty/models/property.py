from odoo import api, fields, models, _

class PropertyModel(models.Model):
    _inherit = "estate.model"

    ptype = fields.Selection([('Condo','Condo'),('Apartment','Apartment'),('Villa','Villa')], string="Property Type",required=True)
    padd = fields.Text("Property Address")
    pdate = fields.Date("Property Last Bought On")
from odoo import api, fields, models, _


class DemoModel(models.Model):
    _name = "demo.modal"
    _description = "Demo Modal"
    _rec_name = "fname"

    fname = fields.Char(string="First Name", required=True)
    lname = fields.Char(string="Last Name")
    description = fields.Text(string="Description")
    address = fields.Text(string="Address")
    is_boolean = fields.Boolean(string="Boolean")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", default="male")
    image = fields.Binary(string="Image")
    add_count = fields.Integer(compute='compute_address',string='Address Character Count',store=True)

    @api.onchange('is_boolean')
    def onchange_is_boolean(self):
        if self.is_boolean:
            self.description = "Sigma"
        else:
            self.description = "Alpha"

    @api.depends("address")
    def compute_address(self):
        # logger.info("----------%r---------",self)
        for rec in self:
            if rec.address:
                rec.add_count = len(rec.address)
            else:
                rec.add_count = 0
    

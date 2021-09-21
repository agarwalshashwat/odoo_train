from typing import DefaultDict
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class EstateModel(models.Model):
    _name = "estate.model"
    _description = "Enlist your on sale property here for better prices"
    _rec_name = "title"

    title = fields.Text(string="Title", required=True)
    ptype = fields.Selection([('Condo','Condo'),('Apartment','Apartment')], string="Property Type",required=True)
    pcode = fields.Char(string="Postal Code",required=True)
    room = fields.Integer(string='Bedrooms')
    lasqm = fields.Float(string='Living Area(sqm)',required=True)
    exp = fields.Float(string='Expected Price',required=True)
    sp = fields.Float(compute="sellvalue",string='Selling Price')
    state = fields.Selection([('nfs','Not For Sale'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold')], string='State', default='nfs')
    availfr = fields.Date(string="Available From")
    soldon = fields.Date(string="Sold On", default=date.today())
    best = fields.Float(compute="bestoffervalue",string='Best Offer')

    desc = fields.Text(string="Description")
    desc_count = fields.Integer(compute='descr_count', string="Description Count",store=True)
    fasc = fields.Integer(string="Fascades")
    garg = fields.Boolean(string="Garage")
    gard = fields.Boolean(string="Garden")
    tasqm = fields.Float(compute="totalareasqm",string="Total Area(sqm)")
    gasqm = fields.Float(string="Garden Area(sqm)")

    buy = fields.One2many(comodel_name='estate.offers',inverse_name="buy_fetch",string="Buyer")

    nfs_reason = fields.Char("Out of Sale Reason")

    estate_desc_ids = fields.Many2many(comodel_name="estate.model.desc",relation="estate_desc_relation",column1="estate_id",column2="estate_desc_id", string="Tags")

    @api.depends("buy")
    def bestoffervalue(self):
        for rec in self:
            rec.best = 0
            for offer in rec.buy:
                # _logger.info("=========Search==========%r---------------------",offer.offer)
                if offer.offer > rec.best:
                    rec.best = offer.offer
                    rec.state = "offer_received"
    
    @api.depends("buy")
    def sellvalue(self):
        for rec in self:
            rec.sp = 0
            for offer in rec.buy:
                # _logger.info("=========Search==========%r---------------------",offer.offer)
                if offer.state == "Accepted":
                    rec.sp = offer.offer

    @api.depends("lasqm","gasqm")
    def totalareasqm(self):
        for rec in self:
            rec.tasqm = 0
            if rec.gasqm:
                var = rec.mapped(lambda x: x.lasqm + x.gasqm)
                _logger.info("=========Search==========%r---------------------",var)
                rec.write({
                    "tasqm" : var[0],
                })
            else:
                rec.write({
                    "tasqm":rec.lasqm,
                })           

    @api.constrains("title")
    def _checktitle_(self):
        for rec in self:
            objs = self.search([("title",'=',rec.title),("id", "!=", self.id)])
            if objs:
                raise ValidationError(_("You cannot create two different profiles for the same property."))

    def action_negotiate(self): 
        for rec in self:
            if rec.buy:
                non_negotiating_offers = rec.buy.filtered(lambda x:x.state != "Negotating")
                if non_negotiating_offers:
                    non_negotiating_offers.write({
                        "state":"Negotiating"
                    })

            

    @api.onchange("garg","gard","fasc")
    def gard_garg(self):
        # prev = self.desc
        # prev_ind = prev.index("The property")-1
        # prev = prev[:prev_ind] + " "
        if self.garg & self.gard:
            self.desc = "The property has Garage and Garden only."
        elif self.gard:
            self.desc = "The property has Garden only."
        elif self.garg:
            self.desc = "The property has Garage only."
        else:
            self.desc = "The property doesn't has Garage and Garden facility."


    @api.depends("desc")
    def descr_count(self):
        for rec in self:
            if rec.desc:
                rec.desc_count = len(rec.desc)
            else:
                rec.desc_count = 0


    # def action_nfs(self):
    #     self.state = "nfs"

    def action_offer_received(self):
        self.state = "offer_received"

    def action_offer_accepted(self):
        self.state = "offer_accepted"

    def action_sold(self):
        self.state = "sold"
    
    def add_profile(self):
        obj = self.env['estate.model.sub'].create({
            "name": self.title,
            "cost": self.sp,
            "type": self.ptype,
            "intro": self.desc,
            "sub_id": self.id
        })

    def update_profile(self):
        obj = self.env["estate.model.sub"].search([('sub_id','=',self.id)])
        if obj:
            obj.write({
                "name": self.title,
                "cost": self.sp,
                "type": self.ptype,
                "intro": self.desc,
            })
            
    def delete_profile(self):
        obj = self.env['estate.model.sub'].search([('sub_id','=',self.id)])
        if obj:
            obj.unlink()
    
    def action_nfs(self):
        self.state = "nfs"
        return {
            'name':_("Cancel Reason"),
            'view_mode': 'form',
            # 'view_id': self.env.ref("demo_module.demo_wizard_form_view").id,
            'res_model': 'estate.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class EstateModelSub(models.Model):
    _name = "estate.model.sub"
    _description = "Estate Model Submenu"

    name = fields.Char("Property Name")
    cost = fields.Float("Cost of Property")
    type = fields.Char("Property Type")
    intro = fields.Text("Property Intro")
    sub_id = fields.Integer("Property Id")

class EstateModelDescription(models.Model):
    _name = "estate.model.desc"
    _description = "Estate Model Tags"

    name = fields.Char(string="Description")
    color = fields.Integer()

class EstateOffers(models.Model):
    _name = "estate.offers"
    _description = "All the offers ever made by the buyers on a particular property"

    buy_fetch = fields.Many2one("estate.model",string="Buyer's Name")
    buy_name = fields.Many2one("demo.model",string="Buyer's Name")
    offer = fields.Float(string="Offer")
    state = fields.Selection([('Accepted','Accepted'),('Negotiating','Negotiating'),('Refused','Refused')],string="Status",required=True,default="Negotiating")
    prop_id = fields.Integer(related="buy_fetch.id", string="Property ID")
    # main_state = fields.Char()

    @api.constrains("state","buy_fetch")
    def _checkofferstatus_(self):
        for rec in self:
            objs = self.search([("state",'=',"Accepted"),("id","!=",rec.id),("buy_fetch.id","=",rec.buy_fetch.id)])
            _logger.info("=========Search==========%r---------------------",objs)
            if objs and rec.state == "Accepted":
                # _logger.info("=========Search==========%r---------------------",self.state)
                raise ValidationError(_("You cannot accept mutiple offers."))

    def action_accept(self):
        self.buy_fetch.state = "offer_accepted" 
        for rec in self:
            objs = self.search([("id","!=",rec.id),("buy_fetch.id","=",rec.buy_fetch.id)])
            var = rec.buy_fetch.buy
            if objs:
                objs.write({
                    "state":"Refused"
                })
        self.state = "Accepted"

    # @api.constrains("main_state","buy_fetch")
    # def _checkofferstatus_(self):
    #     for rec in self:
    #         objs = self.search([("buy_fetch.id","=",rec.buy_fetch.id)])
    #         if rec.buy_fetch.state == "sold":
    #             _logger.info("=========Search==========%r---------------------",rec.buy_fetch.state)
    #             objs.write({
    #                 "main_state" : "sold",
    #             })
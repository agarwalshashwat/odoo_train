# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

GENDER = [('male', 'Male'), ('female', 'Female')]

class DemoModel(models.Model):
    _name = "demo.model"
    _description = "Demo Model"
    _rec_name = "name1"

    name1 = fields.Char(string="Name", required=True, help="Help string.")
    description = fields.Text(string="Description")
    is_boolean = fields.Boolean(string="Boolean")
    gender = fields.Selection(GENDER, string="Gender", default="male")
    image = fields.Binary(string="Image")
    age = fields.Integer(string="Age", default=20)
    weight = fields.Float(string="Weight")
    html_field = fields.Html(string="Html Field")
    char_count = fields.Integer(compute="_compute_char_count", string="Char Count", store=True)
    new_gender = fields.Selection(GENDER, related="gender", string="New Gender", store=True)
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved'), ('canceled', 'Canceled')], string="State", default='draft')
    active = fields.Boolean("Active", default=True)

    tab1_field = fields.Char("Tab1 Field")
    tab2_field = fields.Char("Tab2 Field")
    tab3_field = fields.Char("Tab3 Field")
    tab4_field = fields.Char("Tab4 Field")

    # relational fields
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    email = fields.Char(related="partner_id.email", string="Email")

    skill_ids = fields.One2many(comodel_name="demo.model.skill", inverse_name="demo_model_id", string="Skills")

    tag_ids = fields.Many2many(comodel_name="res.partner.category", relation="demo_moddel_tag_relation", column1="demo_model_id", column2="tag_id", string="Tags")



    @api.onchange("is_boolean")
    def onchnage_is_boolean(self):
        if self.is_boolean:
            self.description = "Boolean field has been set."
        else:
            self.description = "Boolean field has been not set."

    @api.depends("description", "partner_id.email")
    def _compute_char_count(self):
        _logger.info("-----------------%r----------", [self, self.env.context])
        for rec in self:
            if rec.description:
                rec.char_count = len(rec.description)
            else:
                rec.char_count = 0
    
    def action_pending(self):
        self.state = "pending"

    def action_approved(self):
        self.state = "approved"

    def action_canceled(self):
        self.state = "canceled"

    def action_draft(self):
        self.state = "draft"

    def add_skill(self):
        obj = self.env["demo.model.skill"].create({
            "name": self.name1,
            "model_id_db": self.id,
        })

    def search_skill(self):
        objs1 = self.env["demo.model.skill"].search([])

        objs2 = self.env["demo.model.skill"].search([('model_id_db', '=', self.id)])

        obj3 = self.env["demo.model.skill"].browse([1,2,3])

        _logger.info("=========Search==========%r---------------------", [objs1, objs2])

    def update_skill(self):
        objs2 = self.env["demo.model.skill"].search([('model_id_db', '=', self.id)])
        if objs2:
            objs2.write({
                "name": "Hello",
            })

    def unlink_skill(self):
        objs = self.env["demo.model.skill"].search([('model_id_db', '=', self.id)])
        if objs:
            objs.unlink()

    

class DemoModelSkill(models.Model):
    _name = "demo.model.skill"
    _description = "Demo Model Skill"

    name = fields.Char("Skill Name")
    model_id_db = fields.Integer("Demo Model ID")
    demo_model_id = fields.Many2one("demo.model", string="Demo Model")


    # def create(self, vals)

    # create, write, search, browse, unlink

    
    


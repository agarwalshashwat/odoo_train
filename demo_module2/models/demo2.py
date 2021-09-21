# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class DemoModel(models.Model):
    _name = "demo.model"
    _inherit = ["demo.model", 'mail.thread', 'mail.activity.mixin']


    # gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender", default="female")
    gender = fields.Selection(selection_add=[('other', 'Other')], string="Gender", default="female")
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")


    def action_draft(self):
        super(DemoModel, self).action_draft()
        for rec in self:
            rec.html_field = "Set to draft"

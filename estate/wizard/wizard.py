# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class EstateWizard(models.TransientModel):
    _name = "estate.wizard"
    _description = "Estate Wizard"


    reason = fields.Char("Reason", required=True)

    def action_cancel(self):
        self.ensure_one()
        _logger.info("------------------%r-----------------", self.env.context)
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", 0)
        if active_model == "estate.model" and active_id:
            active_obj = self.env["estate.model"].browse(active_id)
            if active_obj:
                # active_obj.nfs_reason = self.reason
                # active_obj.state = "nfs"

                active_obj.write({
                    "nfs_reason": self.reason,
                    "state":"nfs",
                })

    


from odoo import api,fields,models,_
import logging
_logger = logging.getLogger(__name__)

class SchoolFeeWizard(models.TransientModel):
    _name = "school.fee.wizard"
    _description = "School Fee Wizard"

    curr_payment = fields.Float(string="Current Payment",required=True)
    curr_time = fields.Date(string="Date Paid On",required=True)


    def action_payment_register(self):
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", 0)
        if self.curr_payment and self.curr_time and active_id and active_model == "school.fee":
            self.env["school.fee.line"].create({
                "student_fee": active_id,
                "curr_payment": self.curr_payment,
                "paid_on": self.curr_time,
            })
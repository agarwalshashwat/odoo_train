from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class SchoolStudentModel(models.Model):
    _name = "school.student"
    _inherit = ['mail.thread','mail.activity.mixin']
    # _description = "School students data"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Address")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID", domain="[('country_id','=',country_id)]")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("new","New"),("current","Current"),("passout","Pass Out")], string="State",default="new")
    course_id = fields.Many2one(comodel_name="school.course",relation="student_course_relation",column1="studentid",column2="courseid", string = "Course ID",required=True)
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="student_subject_relation",column1="studentid",column2="subjectid", string = "Subject IDs")
    current_user = fields.Many2one('res.users','Profile created by', default = lambda self: self.env.user.id)

    def action_new(self):
        self.state = "new"

    def action_passout(self):
        self.state = "passout"

    def action_current(self):
        self.state = "current"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            # _logger.info("===========Search-----%r-------",rec.date_of_birth)
            # today = datetime.date.today()
            # dob = rec.date_of_birth
            if rec.date_of_birth:
                # _logger.info("===========Search-----%r---%r----",date.today().year -  rec.date_of_birth.year.year, rec.date_of_birth)
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    def returndata(self):
        return {
            "age": self.age,
            "city": self.city
        }

    # @api.constrains("course_id")
    # def studentcourseids(self):
    #     for rec in self:
    #         for course in rec.course_id:
    #             _logger.info("===========Search-----%r---%r-",rec.course_id.id,course.id)
    #             obj = self.env["school.course"].search([('id','=',rec.course_id.id)])
    #             if obj:
    #                 obj.write({
    #                     "student_ids": self.name,
    #                 })

class SchoolTeacherModel(models.Model):
    _name = "school.teacher"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Address")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID" , domain="[('country_id','=',country_id)]")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("active","Active"),("inactive","Inactive")], string="State")
    course_ids = fields.Many2many(comodel_name="school.course",relation="teacher_course_relation",column1="teacherid",column2="courseid", string = "Course IDs")
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="teacher_subject_relation",column1="teacherid",column2="subjectid", string = "Subject IDs")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")

    def action_active(self):
        self.state = "active"

    def action_inactive(self):
        self.state = "inactive"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            if rec.date_of_birth:
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    # @api.o("course_ids")
    # def teachercourseids(self):
    #     for rec in self:
    #         for course in rec.course_ids:
    #             # for id in course:
    #             _logger.info("===========Search-----%r---%r-",rec.course_ids.id,course.id)
    #             obj = self.env["school.course"].search([('id','=',rec.course_ids.id)])
    #             if obj:
    #                 obj.write({
    #                     "teacher_ids": self.name,
    #                 })

class SchoolCourseModel(models.Model):
    _name = "school.course"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    duration = fields.Integer(string="Duration")
    duration_time = fields.Selection([("w","Weeks"),("mo","Months"),("y","Years")], string="Duration Time")
    fee = fields.Integer(string="Fee",required=True)
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")
    position = fields.Char(string="Position/Designation")
    teacher_ids = fields.Many2many(compute="teacher_records",comodel_name="school.teacher",relation="teachercourserelation",column1="teacherid",column2="courseid",string="Teacher's Name")
    student_ids = fields.One2many("school.student",inverse_name="course_id",string="Student's Name")

    new_teacher_ids = fields.Many2many(comodel_name="school.teacher",relation="teacher_course_relation",column1="courseid",column2="teacherid")
    
    # @api.depends("teacher_ids")
    # def teacher_records(self):
    #     for rec in self:
    #         objs = self.env["school.teacher"].search([("course_ids","=",rec.id)])
    #         _logger.info("===========Search-----%r---",objs)
    #         if objs:
    #             rec.teacher_ids = objs.ids
    #         else:
    #             rec.teacher_ids = False


class SchoolSubjectModel(models.Model):
    _name = "school.subject"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")

class SchoolFeesModel(models.Model):
    _name = "school.fee"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student",string="Student ID",required=True)
    total_fee = fields.Float(compute="TotalFee",string="Total Fees")
    due_fee = fields.Float(compute = "DuesCalculator", string="Due Fees")
    amount_paid = fields.Float(compute="AmountPaidCalculator", string="Amount Paid")
    course_id = fields.Many2one("school.course",string="Course ID", domain="[('student_ids','=',student_id)]")

    student_fee_line = fields.One2many(comodel_name="school.fee.line",inverse_name="student_fee",column1="feeid",column2="feeline")
    # @api.depends(course_id)
    # def TotalFee(self):
    #     for rec in self:
    #         rec.total_fee = 0
    #         if 
    @api.depends("course_id")
    def TotalFee(self):
        # self.ensure_one()
        for rec in self:
            rec.total_fee = 0
            if rec:
                rec.write({
                    "total_fee": rec.course_id.fee,
                })

    @api.depends("student_id")
    def AmountPaidCalculator(self):
        for rec in self:
            rec.amount_paid = 0
            if rec.student_id:
                _logger.info("===========Search-Objs-First-----%r----",rec.student_id.id)
                objs = self.env["school.fee.line"].search([("student_fee","=",rec.id)])
                for obj in objs:
                    _logger.info("===========Search-Objs-----%r--%r--",obj.curr_payment,rec.id)
                    rec.write({
                        "amount_paid" : rec.amount_paid + obj.curr_payment,
                    })

    @api.depends("total_fee","amount_paid")
    def DuesCalculator(self):
        for rec in self:
            rec.due_fee = 0
            if rec.total_fee and rec.amount_paid:
                rec.write({
                    "due_fee" : rec.total_fee - rec.amount_paid,
                })

    def action_register_payment(self):
        return{
            "name":("Register Payment"),
            "view_mode":"form",
            "res_model":"school.fee.wizard",
            "type":"ir.actions.act_window",
            "target":"new",
        }
    
    @api.constrains("student_id")
    def _checktitle_(self):
        for rec in self:
            objs = self.search([("student_id",'=',rec.student_id.id),("id", "!=", self.id)])
            if objs:
                raise ValidationError(_("You cannot create two payment profiles for same student"))

class SchoolFeeLineModel(models.Model):
    _name="school.fee.line"
    _rec_name = "student_fee"

    @api.model
    def _get_default_fee_sequence(self):
        return self.env["ir.sequence"].next_by_code("fee.sequence")

    student_fee = fields.Many2one("school.fee")
    payment_id = fields.Char(string="Receipt Number",default=_get_default_fee_sequence)
    curr_payment = fields.Float(string="Payment")
    due_feeline = fields.Float(string="Remaining")
    paid_on = fields.Date(string="Paid On")
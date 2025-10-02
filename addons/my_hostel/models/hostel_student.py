from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

# ctrl + ù

class HostelStudent(models.Model):
    _name = "hostel.student"
    name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"),
    ("female", "Female"), ("other", "Other")],
    string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True,
    help="Activate/Deactivate hostel record")
    room_id = fields.Many2one("hostel.room", "Room",
    help="Select hostel room")

    # computed attributes
    admission_date = fields.Date("Admission Date",
    help="Date of admission in hostel",
    default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date",
    help="Date on which student discharge")
    duration = fields.Integer("Duration", compute="_compute_check_duration",
    inverse="_inverse_duration", help="Enter duration of living")
    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Method to check duration"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days
    def _inverse_duration(self):
        for stu in self:
            duration = -1
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
            if duration != stu.duration:
                stu.discharge_date = (stu.admission_date +
                timedelta(days=stu.duration)).strftime('%Y-%m-%d')

    #related attributes
    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')

    status = fields.Selection([("draft", "Draft"),
    ("reservation", "Reservation"), ("pending", "Pending"),
    ("paid", "Done"),("discharge", "Discharge"), ("cancel", "Cancel")],
    string="Status", copy=False, default="draft",
    help="State of the student hostel")

    def action_assign_room(self):
        self.ensure_one()
        if self.status != "paid":
            raise UserError(_("You can't assign a room if it's not paid."))
        
        room_as_superuser = self.env['hostel.room'].sudo()

        room_rec = room_as_superuser.create({
        "name": "Room A-103",
        "room_no": "A-103",
        "floor_no": 1,
        "room_category_id": self.env.ref("my_hostel.single_room_categ").id,
        "hostel_id": self.hostel_id.id,
        })



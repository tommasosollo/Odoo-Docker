from odoo import models, fields

class HostelRoomMembers(models.Model):
    _name = "hostel.room.members"
    _description = "Hostel Room Members"

    # room_id = fields.Many2one("hostel.room", string="Room", required=True)
    # student_id = fields.Many2one("hostel.student", string="Student", required=True)
    # admission_date = fields.Date("Admission Date")
    # discharge_date = fields.Date("Discharge Date")

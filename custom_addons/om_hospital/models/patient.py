from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient Master"
    _inherit = 'mail.thread'

    name = fields.Char(
        string="Name", 
        required=True, 
        tracking=True
        )

    date_of_birth = fields.Date(
        string="DOB", 
        tracking=True
        )

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], 
        string="Gender", 
        tracking=True
        )


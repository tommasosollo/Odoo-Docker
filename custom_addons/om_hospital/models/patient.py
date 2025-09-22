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

    tag_ids = fields.Many2many(
        'patient.tag',          #co-model
        'patient_tag_rel',      #table name (optional)
        'patient_id',           #patient id (optional)
        'tag_id',               #tag id (optional)
        string="Tags"
    )

    appointment_ids = fields.One2many(
        'hospital.appointment',
        'patient_id',
        string="Appointments"
    )
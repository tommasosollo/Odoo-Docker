from odoo import models, fields, api


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(default=10)
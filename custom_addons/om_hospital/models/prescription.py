from odoo import models, fields, api


class PatientPrescription(models.Model):
    _name = "patient.prescription"
    _description = "Patient Prescription"

    reference = fields.Char(string="Reference", default="New")

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    product_id = fields.Many2one("product.product", string="Drug", required=True)
    qty = fields.Float(string="Quantity", default=1.0)
    note = fields.Text(string="Note")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('patient.prescription')
        return super().create(vals_list)
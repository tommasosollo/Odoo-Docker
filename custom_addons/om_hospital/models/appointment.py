from odoo import models, fields, api
from odoo.exceptions import UserError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread']
    _rec_name = 'patient_id'
    _rec_name_search = ['reference', 'patient_id']

    reference = fields.Char(string="Reference", default="New")
    patient_id = fields.Many2one("hospital.patient", string="Patient", ondelete="restrict")
    appointment_date = fields.Date(string="Date")
    note = fields.Text(string="Note")

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('ongoing', 'Ongoing'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        default="draft",
        tracking=True
    )

    prescription_drugs_ids = fields.One2many(
        "patient.prescription",
        "appointment_id",
        string="Prescription"
    )

    total_qty = fields.Float(compute="_compute_total_qty", string="Total Quantity")

    date_of_birth = fields.Date(related="patient_id.date_of_birth")



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)
    
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

    @api.depends("prescription_drugs_ids.qty")
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(rec.prescription_drugs_ids.mapped("qty"))

    def action_confirm(self):
        for rec in self:
            rec.state='confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state='ongoing'

    def action_done(self):
        for rec in self:
            rec.state='done'

    def action_cancel(self):
        for rec in self:
            rec.state='cancelled'

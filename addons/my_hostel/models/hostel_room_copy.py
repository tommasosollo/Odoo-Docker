from odoo import fields, models, api, _

class HostelRoomCopy(models.Model):
    _name = "hostel.room.copy"
    _inherit = "hostel.room"
    _description = "Hostel Room Information Copy"

    hostel_amenities_ids = fields.Many2many(
        "hostel.amenities",
        "hostel_room_copy_amenities_rel",  # <-- nuova tabella
        "room_copy_id",                    # <-- nuovo campo id
        "amenity_id",                      # <-- colonna amenity
        string="Amenities",
        domain="[('active', '=', True)]",
        help="Select hostel room amenities"
    )

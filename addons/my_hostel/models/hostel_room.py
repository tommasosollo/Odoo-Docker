from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.translate import _


class HostelArchive(models.AbstractModel):
    _name = 'hostel.archive'
    _description = 'Custom Archive for Hostel'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class HostelRoom(models.Model):
    _name = "hostel.room"
    _inherit = ['hostel.archive']
    _description = "Hostel Room"

    name = fields.Char("Room Name")
    room_num = fields.Char("Room No.")
    room_floor = fields.Char("Room Floor")

    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month")

    hostel_id = fields.Many2one("hostel.hostel", "Hostel", help="Name of hostel")
    student_ids = fields.One2many("hostel.student", "room_id",
                                  string="Students", help="Enter students")

    hostel_amenities_ids = fields.Many2many(
        "hostel.amenities",
        "hostel_room_amenities_rel",
        "room_id",
        "amenity_id",
        string="Amenities",
        domain="[('active', '=', True)]",
        help="Select hostel room amenities"
    )

    category_id = fields.Many2one(
        'hostel.category',
        string='Category',
        ondelete='restrict',
        help='Select room category'
    )


    _sql_constraints = [
        ("room_no_unique", "unique(room_num)", "Room number must be unique!")
    ]

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        for rec in self:
            if rec.rent_amount < 0:
                raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

    student_per_room = fields.Integer(
        "Student Per Room",
        required=True,
        default=1,
        help="Students allocated per room"
    )

    availability = fields.Float(
        compute="_compute_check_availability",
        store=True,
        string="Availability",
        help="Room availability in hostel"
    )

    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids)


    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
        ('available', 'closed'),
        ('closed', 'draft')]
        return (old_state, new_state) in allowed
    
    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)
    
    def make_available(self):
        self.change_state('available')
    def make_closed(self):
        self.change_state('closed')
    def make_draft(self):
        self.change_state('draft')


    def log_all_room_members(self):
        # This is an empty recordset of model hostel.room.members
        hostel_room_obj = self.env['hostel.room.members']
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True
    
    def update_room_no(self):
        self.ensure_one()
        self.room_num = "RM002"

    def find_room(self):
        domain = [
            '|',
            '&', ('name', 'ilike', 'Room Name'),
            ('category_id.name', 'ilike', 'Category Name'),
            '&', ('name', 'ilike', 'Second Room Name 2'),
            ('category_id.name', 'ilike', 'SecondCategory Name 2')
        ]
        rooms = self.search(domain)

        UserError(rooms)

    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
            return False
        
        return all_rooms.filtered(predicate)

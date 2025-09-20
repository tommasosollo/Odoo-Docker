from odoo import models, fields, api

class HostelCategory(models.Model):
    _name = "hostel.category"
    name = fields.Char('Category')
    description = fields.Char('Description')
    parent_id = fields.Many2one(
    'hostel.category',
    string='Parent Category',
    ondelete='restrict',
    index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
    'hostel.category', 'parent_id',
    string='Child Categories')
    _parent_store = True
    _parent_name = "parent_id" # optional if field is 'parent_id'
    parent_path = fields.Char(index=True, unaccent=False)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
            'Error! You cannot create recursive categories.')
    
    def create_categories(self):
        categ1 = {
        'name': 'Child category 1',
        'description': 'Description for child 1'
        }

        categ2 = {
        'name': 'Child category 2',
        'description': 'Description for child 2'
        }

        parent_category_val = {
        'name': 'Parent category',
        'description': 'Description for parent category',
        'child_ids': [
        (0, 0, categ1),
        (0, 0, categ2),
        ]
        }

        record = self.env['hostel.category'].create(parent_category_val)


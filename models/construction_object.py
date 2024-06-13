from odoo import fields, models


class ConstructionObject(models.Model):
    _name = 'construction.object'
    _description = 'List of objects'

    name = fields.Char('object name', required=True)

from odoo import api, fields, models


class Location(models.Model):
    _inherit = 'stock.location'

    usage = fields.Selection(
        selection_add=[('construction', 'Construction')],
        ondelete={'construction': 'cascade'}
    )


class StockPickingtype(models.Model):
    _inherit = 'stock.picking.type'

    code = fields.Selection(
        selection_add=[('construction', 'Construction')],
        ondelete={'construction': 'cascade'}
    )


class StockPicking(models.Model):
    _inherit = "stock.picking"

    transport = fields.Many2one("fleet.vehicle", string="Transport Vehicle")
    report_id = fields.Many2one("construction.report", string="Report Number")

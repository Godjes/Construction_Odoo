from odoo import fields, models


class ProductAriival(models.Model):
    _name = 'product.arrival'
    _description = 'Product Arrival'

    quantity = fields.Float('Arrival Quantity', required=True)

    product_id = fields.Many2one(
        'product.template',
        string='Product Name',
        required=True
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Sender',
        required=True
    )
    report_id = fields.Many2one(
        'construction.report',
        string='Report Number',
        ondelete='cascade'
    )
    product_state = fields.Many2one(
        'construction.report.stage',
        string='Report Status',
        related='report_id.stage_id'
    )


class ProductConsumption(models.Model):
    _name = 'product.consumption'
    _description = 'Consumption Product'

    quantity = fields.Float(
        'Consumption Quantity',
        required=True
    )
    product_id = fields.Many2one(
        'product.template',
        string='Product Name',
        required=True
    )
    report_id = fields.Many2one(
        'construction.report',
        string='Report Number',
        ondelete='cascade'
    )
    write_off = fields.Float(
        'Product Written Off',
        defualt=0.0
    )
    product_state = fields.Many2one(
        'construction.report.stage',
        string='Report Status',
        related='report_id.stage_id'
    )

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ConstructionReport(models.Model):
    _name = "construction.report"
    _description = "Report on Work Done"
    _inherit = ["mail.thread",]

    date = fields.Date(
        "Report Date",
        default=fields.Date.today()
    )
    responsible_user_id = fields.Many2one(
        "res.users",
        string="Responsible User",
        default=lambda self: self.env.user
    )
    weather_conditions = fields.Selection([
        ("sunny", "Sunny"),
        ("partly_cloudy", "Partly cloudy"),
        ("rain", "Rain"),
        ("snow", "Snow"),
        ("fog", "Fog"),
    ], string="Weather Conditions")

    time_total_ids = fields.One2many(
        "construction.report.lines",
        "report_id"
        )

    customer = fields.Char("Customer")
    work_line_ids = fields.One2many(
        "construction.report.lines",
        "report_id", string="Work Lines",
        group_operator="sum"
    )
    stage_id = fields.Many2one(
        "construction.report.stage",
        default=lambda self:
        self.env.ref("construction.stage_new"),
        tracking=True
    )
    construction_object_ids = fields.Many2one(
        "construction.object", string="Object Of Construction"
    )
    product_arrival_ids = fields.One2many(
        "product.arrival", "report_id", string="Product  Arrival",
        group_operator="sum"
    )
    product_consumption_ids = fields.One2many(
        "product.consumption", "report_id", string="Product  Consumption"
    )
    time_total_hours = fields.Float(
        "Total Hours",
        compute="_compute_time_total_hours",
        store=True
    )

    @api.depends('time_total_ids.time_total')
    def _compute_time_total_hours(self):
        for report in self:
            report.time_total_hours = sum(report.time_total_ids.mapped('time_total'))


    def action_after_aprove(self):
        self._consumptions_picking()
        self._arrives_picking()
        self.action_approve_report()

    def action_submit_for_approval(self):
        review_stage = self.env.ref("construction.stage_review")
        self.write({"stage_id": review_stage.id})

    def action_approve_report(self):
        approved_stage = self.env.ref("construction.stage_approved")
        self.write({"stage_id": approved_stage.id})

    def _consumptions_picking(self):
        datas = []
        for line in self.product_consumption_ids:
            if line.quantity and line.product_id:
                datas.append(
                    {
                        "construction_consumption_id": line.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.quantity,
                        "location_id": 19,
                        "location_dest_id": self.env.ref("construction.construction_location").id,
                        "name": "test_add",
                    }
                )
        if datas:
            picking_id = self.env["stock.picking"].create(
                {
                    "picking_type_id": self.env.ref("construction.construction_write_off").id,
                    "report_id": self.id,
                    "location_id": 19,
                    "location_dest_id": self.env.ref("construction.construction_location").id,
                    "move_ids_without_package": [(0, 0, vals)for vals in datas]

                }
            )
            product_qty_move_ids = {
                record.construction_consumption_id.id: record.product_uom_qty for record in picking_id.move_ids_without_package
            }
            picking_id.action_confirm()

            for rec in picking_id.move_ids_without_package:
                rec.quantity_done = rec.reserved_availability

            picking_id.button_validate()
            self._update_write_off_field(self.product_consumption_ids, product_qty_move_ids)

    def _update_write_off_field(self, product_consumption_ids, product_qty_move_ids):

        for consumption in product_consumption_ids:

            consumption.write_off = product_qty_move_ids.get(
                consumption.id, 0
            )

    def _arrives_picking(self):
        datas = []
        for line in self.product_arrival_ids:

            if line.quantity and line.product_id:
                datas.append(
                    {
                        "product_id": line.product_id.id,
                        "product_uom_qty": line.quantity,
                        "location_id": line.location_id.id,
                        "location_dest_id": 19,
                        "name": "test_add",
                    }
                )
        if datas:

            picking_id = self.env["stock.picking"].create(
                {
                    "picking_type_id": self.env.ref("construction.construction_write_off").id,
                    "report_id": self.id,
                    "location_id": line.location_id.id,
                    "location_dest_id": 19,
                    "move_ids_without_package": [(0, 0, vals)for vals in datas]

                }
            )
            picking_id.action_confirm()
            for rec in picking_id.move_ids_without_package:
                rec.quantity_done = rec.reserved_availability
            picking_id.button_validate()

    @api.constrains("work_line_ids")
    def _check_time_intervals(self):
        """
        Валидация для правильного заполнения времени работ
        """
        for rec in self:
            time_slots = [0] * 24 * 60
            total_time = 0

            for work in rec.work_line_ids:
                if work.time_from < 0.0 or work.time_to > 24.0:
                    raise ValidationError(
                        _(
                            "Time from and time should be basically"
                            "from 0.0 to 24.0"
                        )
                    )

                if work.time_from >= work.time_to:
                    raise ValidationError(
                        _(
                            "Время начала работы должно быть меньше "
                            "времени окончания работы"
                        )
                    )

                start_minutes = int(work.time_from * 60)
                end_minutes = int(work.time_to * 60)

                for minute in range(start_minutes, end_minutes):
                    if time_slots[minute] != 0:
                        raise ValidationError(
                           _("Crossing time slots is not allowed")
                        )
                    time_slots[minute] = 1

                total_time += (work.time_to - work.time_from) * 60

            if total_time != 24 * 60:
                raise ValidationError(
                    _("The total operating time must be 24 hours")
                )

    def name_get(self):
        """
        Возвращет название отчета в формате:
        Отчет за (2024-01-01)
        """
        result = []
        for record in self:
            rec_name = "Report for (%s) (%s)" % (
                record.date, record.stage_id.name)
            result.append((record.id, rec_name))
        return result


class ConstructionReportLines(models.Model):

    _name = "construction.report.lines"
    _description = "Report Lines"

    report_id = fields.Many2one(
        "construction.report",
        "Report"
    )
    work_id = fields.Many2one(
        "construction.work",
        "Work Name",
        required=True
    )
    time_from = fields.Float(
        "Time From",
        digits=(2, 1),
        store=True
    )
    time_to = fields.Float(
        "Time To",
        digits=(2, 1),
        store=True
    )
    time_total = fields.Float(
        "Total Hours",
        compute="_compute_time_total",
        store=True)

    work_category_id = fields.Many2one(
        related="work_id.category_id",
        store=True)

    date = fields.Date(related="report_id.date")

    @api.depends("time_from", "time_to")
    def _compute_time_total(self):
        """Суммарное время выполнения работы"""
        for work in self:
            work.time_total = work.time_to - work.time_from


class ConstructionsWork(models.Model):

    _name = "construction.work"
    _description = "Work List"

    name = fields.Char(
        "Work Name",
        required=True
    )
    description = fields.Text("Work Description")
    category_id = fields.Many2one(
        "construction.category",
        string="Work Category",
    )


class ConstructionReportStage(models.Model):

    _name = "construction.report.stage"
    _description = "Report Stages"
    _order = "sequence, name"

    name = fields.Char()
    sequence = fields.Integer()
    fold = fields.Boolean()
    report_state = fields.Selection([
        ("new", "New"),
        ("review", "Review"),
        ("approved", "Approved"),
    ], "State", default="new")


class ConstructionStockMove(models.Model):

    _inherit = "stock.move"
    construction_consumption_id = fields.Many2one(
        "product.consumption"
    )

from odoo import fields, models


class ConstructionCategory(models.Model):

    _name = "construction.category"
    _description = "Categories for Works"

    name = fields.Char(
        "Category",
        required=True
    )
    work_ids = fields.One2many(
        "construction.work",
        "category_id",
        string="Works")

    works_count = fields.Integer(compute="compute_count")

    def compute_count(self):
        for record in self:
            record.works_count = len(record.work_ids)

    def action_open_works(self):
        """Отображение работ связанных с категорией"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Работы",
            "res_model": "construction.work",
            "view_mode": "tree,form",
            "domain": [("category_id", "=", self.id)],
            "context": {"default_category_id": self.id},
        }

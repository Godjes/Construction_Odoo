from odoo import fields, models


class ConstructionCategory(models.Model):
    """
     Класс для представления категорий работ.
    ...
    Атрибуты
    --------
    _name : str
        название модели в БД
    __description : str
        описание класса
    name : str
        категория работы
    work_ids : int
        работа относящаяся к категории
    Методы
    ------
    action_open_works():
        Отображение работ связанных с категорией
    """
    _name = 'construction.category'
    _description = 'Construction Category'

    name = fields.Char(
        'Название категории',
        required=True
    )
    work_ids = fields.One2many(
        'construction.work.list',
        'category_id',
        string='Работы')

    def action_open_works(self):
        """Отображение работ связанных с категорией"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Работы',
            'res_model': 'construction.work.list',
            'view_mode': 'tree,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }

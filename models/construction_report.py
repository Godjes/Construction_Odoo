from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ConstructionReport(models.Model):
    """
     Класс для представления отчета о работе.
    ...
    Атрибуты
    --------
    _name : str
        название модели в БД
    __description : str
        описание класса
    date : date
        дата заполнения отчета
    responsible : int
        Отвественный за работу
    weather_conditions : str
        Погодные условия
    report : str
        отчет
    customer : str
        заказчик
    Методы
    ------
    _check_time_intervals():
        Валидация введеных данных
    """
    _name = 'construction.report'
    _description = 'Construction Report'

    date = fields.Date(
        'Дата отчета',
        default=fields.Date.today()
    )
    responsible = fields.Many2many(
        'res.users',
        string='Отвественный за работу'
    )
    weather_conditions = fields.Selection([
        ('ясно', 'Ясно'),
        ('пасмурно', 'Пасмурно'),
        ('дождь', 'Дождь'),
        ('снег', 'Снег'),
        ('туман', 'Туман'),
    ], string='Погодные условия')

    customer = fields.Char('Заказчик')
    report = fields.One2many('construction.work', 'report_id')

    @api.constrains('report')
    def _check_time_intervals(self):
        """
        Валидация для правильного заполнения времени работ
        """
        for rec in self:
            time_slots = [0] * 24
            total_time = 0

            for work in rec.report:
                if work.time_from < 0.0 or work.time_to > 24.0:
                    raise ValidationError(
                        "Время от и время до должны быть в диапазоне "
                        "от 0.0 до 24.0"
                    )

                if work.time_from >= work.time_to:
                    raise ValidationError(
                        "Время начала работы должно быть меньше"
                        "времени окончания работы"
                    )
                start_hour = int(work.time_from)
                end_hour = int(work.time_to)
                for hour in range(start_hour, end_hour):

                    if time_slots[hour] != 0:
                        raise ValidationError(
                            "Пересечение временных интервалов не допускается"
                        )
                    time_slots[hour] = 1

                total_time += work.time_total

            if total_time != 24:
                raise ValidationError(
                    "Cуммарное время работы должно быть 24 часа"
                )


class ConstructionWork(models.Model):
    """
     Класс для представления отчета о работе.
    ...
    Атрибуты
    --------
    _name : str
        название модели в БД
    __description : str
        описание класса
    report_id : int
        отчет
    time_from : float
        начало работ
    time_to : float
        окончание работ
    time_total : float
        время работ
    work_name : str
        название работы
    Методы
    ------
    _compute_time_total():
        суммарное время работ
    """
    _name = 'construction.work'
    _description = 'Construction Work'

    report_id = fields.Many2one(
        'construction.report',
        'Отчёт'
    )
    time_from = fields.Float(
        'начало работ',
        digits=(2, 1)
    )
    time_to = fields.Float(
        'Конец работ',
        digits=(2, 1)
    )
    time_total = fields.Float(
        'Время работы',
        compute='_compute_time_total')
    work_name = fields.Char()

    @api.depends('time_from', 'time_to')
    def _compute_time_total(self):
        """Суммарное время выполнения работы"""
        for work in self:
            work.time_total = work.time_to - work.time_from

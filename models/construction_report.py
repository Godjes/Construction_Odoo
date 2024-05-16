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
    weather_conditions : str
        Погодные условия
    work_line_ids : str
        отчет
    customer : str
        заказчик
    responsible_user_id : str
        Отвественный
    Методы
    ------
    _check_time_intervals():
        Валидация введеных данных
    name_get()
        Кастомизирует название отчета
    """
    _name = 'construction.report'
    _description = 'Construction Report'

    date = fields.Date(
        'Дата отчета',
        default=fields.Date.today()
    )
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Ответственный',
        default=lambda self: self.env.user
    )
    weather_conditions = fields.Selection([
        ('sunny', 'Ясно'),
        ('partly_cloudy', 'Пасмурно'),
        ('rain', 'Дождь'),
        ('snow', 'Снег'),
        ('fog', 'Туман'),
    ], string='Погодные условия')

    customer = fields.Char('Заказчик')
    work_line_ids = fields.One2many('construction.work', 'report_id')

    @api.constrains('work_line_ids')
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
                        "Время от и время до должны быть в диапазоне "
                        "от 0.0 до 24.0"
                    )

                if work.time_from >= work.time_to:
                    raise ValidationError(
                        "Время начала работы должно быть меньше "
                        "времени окончания работы"
                    )

                start_minutes = int(work.time_from * 60)
                end_minutes = int(work.time_to * 60)

                for minute in range(start_minutes, end_minutes):
                    if time_slots[minute] != 0:
                        raise ValidationError(
                            "Пересечение временных интервалов не допускается"
                        )
                    time_slots[minute] = 1

                total_time += (work.time_to - work.time_from) * 60

            if total_time != 24 * 60:
                raise ValidationError(
                    "Суммарное время работы должно быть 24 часа"
                )

    def name_get(self):
        """
        Возвращет название отчета в формате:
        Отчет за (2024-01-01)
        """
        result = []
        for record in self:
            rec_name = "Отчет за (%s)" % (record.date)
            result.append((record.id, rec_name))
        return result


class ConstructionReportLines(models.Model):
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
        'Время от',
        digits=(2, 1)
    )
    time_to = fields.Float(
        'Время до',
        digits=(2, 1)
    )
    time_total = fields.Float(
        'Итого часов',
        compute='_compute_time_total')
    work_name = fields.Char('Наименование работы')

    @api.depends('time_from', 'time_to')
    def _compute_time_total(self):
        """Суммарное время выполнения работы"""
        for work in self:
            work.time_total = work.time_to - work.time_from

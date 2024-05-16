from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestConstructionReport(TransactionCase):

    def setUp(self):
        super(TestConstructionReport, self).setUp()
        self.construction_report = self.env['construction.report']
        self.construction_work = self.env['construction.work']

    def test_01_construction_report_name(self):
        """Проверка создания отчета с правильным именем"""
        report = self.construction_report.create({'date': '2022-01-01'})
        self.assertEqual(report.name_get()[0][1], 'Отчет за (2022-01-01)')

    def test_02_construction_work_compute(self):
        """Проверка создания отчета с правильно вычисленным временем работы"""
        work = self.construction_work.create({
            'time_from': 8.0,
            'time_to': 16.0,
            'work_name': 'Test Work'
        })
        self.assertEqual(work.time_total, 8.0)

    def test_03_construction_report_constraints(self):
        """
        Проверка невозможности создания отчета
        0 > время работы > 24.0:
        """
        work_line_ids = [
            [0, 'virtual_13',
                {'time_from': -1, 'time_to': 25, 'work_name': 'fdsfdsfds'}]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                'date': '2022-01-01',
                'responsible_user_id': 2,
                'weather_conditions': 'sunny',
                'customer': 'first',
                'work_line_ids': work_line_ids
                }
            )

    def test_04_construction_report_start_before_end(self):
        """
        Проверка невозможности создания отчета
        время начала > времени окончания:
        """
        work_line_ids = [
            [0, 'virtual_13',
                {'time_from': 24, 'time_to': 0, 'work_name': False}]
            ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                'date': '2022-01-01',
                'responsible_user_id': 2,
                'weather_conditions': 'sunny',
                'customer': 'second',
                'work_line_ids': work_line_ids
                }
            )

    def test_05_construction_report_time_intervals(self):
        """
        Проверка невозможности создания отчета
        с пересечением интервалов времени:
        """
        work_line_ids = [
            [0, 'virtual_23',
                {'time_from': 0, 'time_to': 5, 'work_name': False}],
            [0, 'virtual_24',
                {'time_from': 4, 'time_to': 24, 'work_name': False}]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                'date': '2022-01-01',
                'responsible_user_id': 2,
                'weather_conditions': 'sunny',
                'customer': 'first',
                'work_line_ids': work_line_ids
                }
            )

    def test_06_construction_report_constraints_time_total(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work_line_ids = [
            [0, 'virtual_23',
                {'time_from': 0, 'time_to': 3, 'work_name': False}],
            [0, 'virtual_24',
                {'time_from': 3, 'time_to': 23, 'work_name': False}]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                'date': '2022-01-01',
                'responsible_user_id': 2,
                'weather_conditions': 'sunny',
                'customer': 'first',
                'work_line_ids': work_line_ids
                }
            )

    def test_06_construction_report_constraints_time_total_more_24(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work_line_ids = [
            [0, 'virtual_23',
                {'time_from': 0, 'time_to': 3, 'work_name': False}],
            [0, 'virtual_24',
                {'time_from': 3, 'time_to': 23, 'work_name': False}]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                'date': '2022-01-01',
                'responsible_user_id': 2,
                'weather_conditions': 'sunny',
                'customer': 'first',
                'work_line_ids': work_line_ids
                }
            )

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestConstructionReport(TransactionCase):
    """Тесты для модуля construction"""

    def setUp(self):
        super(TestConstructionReport, self).setUp()
        self.construction_report = self.env['construction.report']
        self.construction_reprot_lines = self.env['construction.report.lines']
        self.Constructions_work_list = self.env['construction.work.list']
        self.Construction_report_stage = self.env['construction.report.stage']
        self.construction_category = self.env['construction.category']

    def test_01_construction_report_name(self):
        """Проверка создания отчета с правильным именем"""
        report = self.construction_report.create({
            'date': '2022-01-01',
            'weather_conditions': 'sunny',
            'customer': 'Test Customer',
        })
        self.assertEqual(report.stage_id.name, 'Новый')

        report.action_submit_for_approval()
        self.assertEqual(report.stage_id.name, 'На согласовании')

        report.action_approve_report()
        self.assertEqual(report.stage_id.name, 'Согласован')

    def test_02_construction_report_lines(self):
        """Проверка создания отчета с правильно вычисленным временем работы"""
        work = self.Constructions_work_list.create({
            'name': 'Test Work',
            'description': 'Test Description',
        })
        report_lines = self.construction_reprot_lines.create({
            'work_id': work.id,
            'time_from': 8.0,
            'time_to': 16.0,
        })
        self.assertEqual(report_lines.time_total, 8.0)

    def test_03_constructions_work_list(self):
        """Проверка создания работы"""
        work = self.Constructions_work_list.create({
            'name': 'Test Work',
            'description': 'Test Description',
        })
        self.assertEqual(work.name, 'Test Work')

    def test_04_construction_report_stage(self):
        """Проверка создания этапа"""
        stage = self.Construction_report_stage.create({
            'name': 'Test Stage',
            'sequence': 1,
            'report_state': 'new',
        })
        self.assertEqual(stage.name, 'Test Stage')

    def test_05_construction_category(self):
        """Проверка создания категории"""
        category = self.construction_category.create({
            'name': 'Test Category',
        })
        self.assertEqual(category.name, 'Test Category')

        action = category.action_open_works()
        self.assertEqual(action['res_model'], 'construction.work.list')
        self.assertEqual(action['context']['default_category_id'], category.id)

    def test_06_construction_report_time_intervals(self):
        """
        Проверка невозможности создания отчета
        с пересечением интервалов времени:
        """
        work_line_ids = [
            [
                0, 'virtual_3',
                {
                    'time_from': 0,
                    'time_to': 5,
                    'work_id': 1
                }
            ],
            [
                0,
                'virtual_4',
                {
                    'time_from': 4,
                    'time_to': 24,
                    'work_id': 2
                    }
            ]
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

    def test_07_construction_report_constraints_time_total(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work_line_ids = [
            [
                0, 'virtual_3',
                {
                    'time_from': 0,
                    'time_to': 3,
                    'work_id': 1
                }
            ],
            [
                0,
                'virtual_4',
                {
                    'time_from': 3,
                    'time_to': 23,
                    'work_id': 2
                    }
            ]
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

    def test_08_construction_report_constraints_time_total_less_24(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work_line_ids = [
            [
                0, 'virtual_3',
                {
                    'time_from': 0,
                    'time_to': 3,
                    'work_id': 1
                }
            ],
            [
                0,
                'virtual_4',
                {
                    'time_from': 3,
                    'time_to': 23,
                    'work_id': 2
                    }
            ]
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

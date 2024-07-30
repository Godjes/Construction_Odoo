from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestConstructionReport(TransactionCase):
    """Тесты для модуля construction"""

    def setUp(self):
        super(TestConstructionReport, self).setUp()
        self.construction_report = self.env["construction.report"]
        self.construction_reprot_lines = self.env["construction.report.lines"]
        self.constructions_work = self.env["construction.work"]
        self.construction_report_stage = self.env["construction.report.stage"]
        self.construction_category = self.env["construction.category"]
        self.construction_object = self.env["construction.object"]
        self.product = self.env["product.template"]

    def test_01_construction_report_name(self):
        """Проверка создания отчета с правильным именем"""
        construction_object = self.construction_object.create(
            {"name": "test_object"}
        )
        report = self.construction_report.create({
            "date": "2022-01-01",
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": construction_object.id
        })

        self.assertEqual(
            report.stage_id.name,
            "New",
            "При создании статус отчета должен быть - 'New"
        )

        report.action_submit_for_approval()
        self.assertEqual(
            report.stage_id.name,
            "Review",
            (
                "При нажатии на кнопку 'отправить на согласование' "
                "статус отчета должен быть 'Review'"
            )
        )

        report.action_approve_report()
        self.assertEqual(
            report.stage_id.name,
            "Approved",
            (
                "При нажатии на кнопку 'согласовать' "
                "статус отчета должен быть 'Approved'"
            )
            )

        self.assertEqual(
            report.construction_object_ids.name, "test_object",
            "Название объекта строительства не совпадает"
            )

    def test_02_construction_report_lines(self):
        """Проверка создания отчета с правильно вычисленным временем работы"""
        work = self.constructions_work.create({
            "name": "Test Work",
            "description": "Test Description",
        })
        report_lines = self.construction_reprot_lines.create({
            "work_id": work.id,
            "time_from": 8.0,
            "time_to": 16.0,
        })
        self.assertEqual(
            report_lines.time_total, 8.0,
            "Время работы не соответствует ожидаемому"
            )

    def test_03_constructions_work_list(self):
        """Проверка создания работы"""
        work = self.constructions_work.create({
            "name": "Test Work",
            "description": "Test Description",
        })
        self.assertEqual(
            work.name, "Test Work",
            "Название работы не совпадает"
        )

    def test_04_construction_report_stage(self):
        """Проверка создания этапа"""
        stage = self.construction_report_stage.create({
            "name": "Test Stage",
            "sequence": 1,
            "report_state": "new",
        })
        self.assertEqual(
            stage.name, "Test Stage",
            "Название этапа не совпадает"
        )

    def test_05_construction_category(self):
        """Проверка создания категории"""
        category = self.construction_category.create({
            "name": "Test Category",
        })
        self.assertEqual(
            category.name, "Test Category",
            "Название категории не совпадает"
            )

        action = category.action_open_works()
        self.assertEqual(
            action["res_model"], "construction.work",
            "Отображаемая модель не соответствует ожидаемой"
        )
        self.assertEqual(
            action["context"]["default_category_id"], category.id,
            "Контекст действия не соответствует ожидаемому"
            )

    def test_06_construction_report_time_intervals(self):
        """
        Проверка невозможности создания отчета
        с пересечением интервалов времени:
        """
        work1 = self.constructions_work.create(
            {
                "name": "Test Work 1",
                "description": "Test Description 1",
            }
        )
        work2 = self.constructions_work.create(
            {
                "name": "Test Work 2",
                "description": "Test Description 2",
            }
        )
        work_line_ids = [
            [
                0, "virtual_3",
                {
                    "time_from": 0,
                    "time_to": 5,
                    "work_id": work1.id
                }
            ],
            [
                0,
                "virtual_4",
                {
                    "time_from": 4,
                    "time_to": 24,
                    "work_id": work2.id
                }
            ]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                "date": "2022-01-01",
                "responsible_user_id": 2,
                "weather_conditions": "sunny",
                "customer": "first",
                "work_line_ids": work_line_ids
                }
            )

    def test_07_construction_report_constraints_time_total(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work1 = self.constructions_work.create(
            {
                "name": "Test Work 1",
                "description": "Test Description 1",
            }
        )
        work2 = self.constructions_work.create(
            {
                "name": "Test Work 2",
                "description": "Test Description 2",
            }
        )
        work_line_ids = [
            [
                0, "virtual_3",
                {
                    "time_from": 0,
                    "time_to": 5,
                    "work_id": work1.id
                }
            ],
            [
                0,
                "virtual_4",
                {
                    "time_from": 4,
                    "time_to": 24,
                    "work_id": work2.id
                }
            ]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                "date": "2022-01-01",
                "responsible_user_id": 2,
                "weather_conditions": "sunny",
                "customer": "first",
                "work_line_ids": work_line_ids
                }
            )

    def test_08_construction_report_constraints_time_total_less_24(self):
        """
        Проверка невозможности создания отчета
        с суммарным временем меньше 24 часов:
        """
        work1 = self.constructions_work.create(
            {
                "name": "Test Work 1",
                "description": "Test Description 1",
            }
        )
        work2 = self.constructions_work.create(
            {
                "name": "Test Work 2",
                "description": "Test Description 2",
            }
        )
        work_line_ids = [
            [
                0, "virtual_3",
                {
                    "time_from": 0,
                    "time_to": 5,
                    "work_id": work1.id
                }
            ],
            [
                0,
                "virtual_4",
                {
                    "time_from": 4,
                    "time_to": 24,
                    "work_id": work2.id
                }
            ]
        ]
        with self.assertRaises(ValidationError):
            self.construction_report.create({
                "date": "2022-01-01",
                "responsible_user_id": 2,
                "weather_conditions": "sunny",
                "customer": "first",
                "work_line_ids": work_line_ids
                }
            )

    def test_09_consumptions_picking(self):
        report = self.env["construction.report"].create({
            "date": "2024-01-01",
            "responsible_user_id": self.env.user.id,
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": self.env["construction.object"].create({
                "name": "Test Construction Object"
            }).id
        })

        product_consumption = self.env["product.consumption"].create({
            "report_id": report.id,
            "product_id": self.env["product.product"].create({
                "name": "Test Product"
            }).id,
            "quantity": 10
        })

        report._consumptions_picking()

        self.assertEqual(
            len(report.product_consumption_ids), 1,
            "Количество записей о потреблении не соответствует ожидаемому"
        )
        self.assertEqual(
            report.product_consumption_ids.write_off, 10,
            "Количество записей о потреблении не соответствует ожидаемому"
        )

    def test_10_arrives_picking(self):
        report = self.env["construction.report"].create({
            "date": "2024-01-01",
            "responsible_user_id": self.env.user.id,
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": self.env["construction.object"].create({
                "name": "Test Construction Object"
            }).id
        })

        product_arrival = self.env["product.arrival"].create({
            "report_id": report.id,
            "product_id": self.env["product.product"].create({
                "name": "Test Product"
            }).id,
            "quantity": 10,
            "location_id": self.env.ref("construction.construction_location").id
        })

        report._arrives_picking()

        self.assertEqual(
            len(report.product_arrival_ids), 1,
            "Количество записей о прибытии не соответствует ожидаемому"
        )
        self.assertEqual(
            report.product_arrival_ids.quantity, 10,
            "Количество записей о прибытии не соответствует ожидаемому"
        )

    def test_11_action_after_approve(self):
        report = self.env["construction.report"].create({
            "date": "2024-01-01",
            "responsible_user_id": self.env.user.id,
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": self.env["construction.object"].create({
                "name": "Test Construction Object"
            }).id
        })

        product_consumption = self.env["product.consumption"].create({
            "report_id": report.id,
            "product_id": self.env["product.product"].create({
                "name": "Test Product"
            }).id,
            "quantity": 10
        })

        product_arrival = self.env["product.arrival"].create({
            "report_id": report.id,
            "product_id": self.env["product.product"].create({
                "name": "Test Product"
            }).id,
            "quantity": 10,
            "location_id": self.env.ref("construction.construction_location").id
        })

        report.action_after_aprove()

        self.assertEqual(
            len(report.product_consumption_ids), 1,
            "Количество записей о потреблении не соответствует ожидаемому"
        )
        self.assertEqual(
            report.product_consumption_ids.write_off, 10,
            "Количество записей о потреблении не соответствует ожидаемому"
        )
        self.assertEqual(
            len(report.product_arrival_ids), 1,
            "Количество записей о прибытии не соответствует ожидаемому"
        )
        self.assertEqual(
            report.product_arrival_ids.quantity, 10,
            "Количество записей о прибытии не соответствует ожидаемому"
        )
        self.assertEqual(
            report.stage_id.name, "Approved",
            "Статус отчета не соответствует ожидаемому"
        )

    def test_12_action_submit_for_approval(self):
        report = self.env["construction.report"].create({
            "date": "2024-01-01",
            "responsible_user_id": self.env.user.id,
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": self.env["construction.object"].create({
                "name": "Test Construction Object"
            }).id
        })

        report.action_submit_for_approval()

        self.assertEqual(report.stage_id.name, "Review")

    def test_13_action_approve_report(self):
        report = self.env["construction.report"].create({
            "date": "2024-01-01",
            "responsible_user_id": self.env.user.id,
            "weather_conditions": "sunny",
            "customer": "Test Customer",
            "construction_object_ids": self.env["construction.object"].create({
                "name": "Test Construction Object"
            }).id
        })

        report.action_approve_report()

        self.assertEqual(
            report.stage_id.name, "Approved",
            "Статус отчета не соответствует ожидаемому"
        )

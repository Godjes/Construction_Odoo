# -*- coding: utf-8 -*-
{
    'name': "Construction",
    'description': """Для отчета о проделанной работе""",
    'author': "Rydlab",
    'website': "https://rydlab.ru/",
    'category': 'Construction',
    'version': '16.0.0.3.1',
    'depends': ['base', 'mail', 'contacts', 'product', 'stock', 'fleet'],
    'data': [
        #'security/groups.xml',
        'security/ir.model.access.csv',
        'views/construction_report.xml',
        'data/report_stage.xml',
        'data/location.xml',
        'data/picking_type.xml',
        'views/construction_category.xml',
        'views/construction_work.xml',
        'views/construction_objects.xml',
        'views/stock.xml'
    ],
}

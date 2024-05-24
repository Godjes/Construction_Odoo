# -*- coding: utf-8 -*-
{
    'name': "Construction",
    'description': """Для отчета о проделанной работе""",
    'author': "Rydlab",
    'website': "https://rydlab.ru/",
    'category': 'Construction',
    'version': '16.0.0.2.1',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        #'security/groups.xml',
        'security/ir.model.access.csv',
        'views/construction_report.xml',
        'data/report_stage.xml',
        'views/construction_category.xml',
    ],
}

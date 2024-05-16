def migrate(cr, version):
    cr.execute('DROP TABLE construction_report_liness')

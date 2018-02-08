# -*- coding: utf-8 -*-
from django.test import TestCase


# Create your tests here.



class XLSXTests(TestCase):
    def test_xlsx(self):
        from portal.excel.excel import ExcelParser

        # filename = 'document_template.xltx'
        # filename = '/Users/liuxue/Downloads/Developer/GoldenTimes/唱片资料20170425.xlsx'
        filename = '/Users/liuxue/Downloads/Developer/GoldenTimes/唱片资料20170425的副本.xlsx'

        parser = ExcelParser(filename=filename)
        parser.parse()

        pass

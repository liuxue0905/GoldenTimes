from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

import os
from datetime import datetime
from portal.models import ExcelLog
from portal.excel.excel import ExcelParser


class Command(BaseCommand):
    def add_arguments(self, parser):
        print('Command', 'add_arguments')

        # Positional arguments
        parser.add_argument('path', nargs='+', type=str)

        # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **options):
        print('Command', 'handle', args, options)

        for path in options['path']:
            try:
                Command.handle_path(path)
            except Exception as e:
                raise CommandError('Error: "%s".' % e)

            self.stdout.write(self.style.SUCCESS('Successfully import path "%s"' % path))

    @staticmethod
    def handle_path(path):
        print('Command', 'handle', 'path', path)

        def make_filename(datetime_now):
            dir_excel = os.path.join(os.path.join(os.path.abspath(settings.MEDIA_ROOT), 'excel'),
                                     datetime_now.strftime("%Y-%m-%d"))
            if not os.path.exists(dir_excel):
                os.makedirs(dir_excel)

            filename_excel = os.path.join(dir_excel, datetime_now.strftime("%Y-%m-%d %H:%M:%S.%f") + '.xlsx')
            filename_log = filename_excel + '.log'

            return filename_excel, filename_log

        datetime_start = datetime.now()

        filename_excel, filename_log = make_filename(datetime_start)

        with open(path, 'rb') as f:
            with open(filename_excel, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        def parse(filename_excel, filename_log):
            excel_log = ExcelLog()
            excel_log.status = ExcelLog.STATUS_START
            excel_log.datetime_start = datetime_start

            try:
                parser = ExcelParser(filename_excel, filename_log)

                excel_log.file_excel.name = os.path.relpath(parser.filename_excel, os.path.abspath(settings.MEDIA_ROOT))
                excel_log.file_log.name = os.path.relpath(parser.filename_log, os.path.abspath(settings.MEDIA_ROOT))

                parser.parse()
            except Exception as e:
                print(e)
                excel_log.status = ExcelLog.STATUS_ERROR
            finally:
                # os.remove(filename)
                excel_log.status = ExcelLog.STATUS_SUCCESS
                excel_log.datetime_end = datetime.now()
                excel_log.save()
                pass

        parse(filename_excel, filename_log)

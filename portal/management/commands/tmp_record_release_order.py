from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

import os
from datetime import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        print('Command', 'add_arguments')

        # Positional arguments
        # parser.add_argument('path', nargs='+', type=str)

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

        try:
            Command.handle_cmd()
        except Exception as e:
            raise CommandError('Error: "%s".' % e)

        self.stdout.write(self.style.SUCCESS('Successfully'))

    @staticmethod
    def handle_cmd():
        print('Command', 'handle')

        from portal.models import Record
        records = Record.objects.all()

        print('==========')
        for record in records:
            release_order = record.release_order
            if release_order:
                if len(release_order) != 8:
                    print('[%s][%s][%s][%s]' % (record.title, record.number, record.year, record.release_order))
        print('==========')

        print('==========')
        for record in records:
            release_order = record.release_order
            if release_order:
                if len(release_order) == 8:
                    if release_order[4:] != '0000':
                        print('[%s][%s][%s][%s]' % (record.title, record.number, record.year, record.release_order))
        print('==========')

        print('==========')
        for record in records:
            release_order = record.release_order
            if release_order:
                if len(release_order) == 8:
                    if release_order[4:6] != '00':
                        print('[%s][%s][%s][%s]' % (record.title, record.number, record.year, record.release_order))
        print('==========')

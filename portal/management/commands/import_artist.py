from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

import os
from datetime import datetime
from portal.models import LogImportArtist
from portal.parser.artist import ArtistParser


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

            return os.path.join(dir_excel, datetime_now.strftime("%Y-%m-%d %H:%M:%S.%f") + '.xlsx')

        datetime_start = datetime.now()
        filename = make_filename(datetime_start)

        with open(path, 'rb') as f:
            with open(filename, 'wb+') as destination:
                destination.write(f.read())
                destination.truncate()
                # for chunk in f.chunks():
                #     destination.write(chunk)

        parser = ArtistParser(filename)
        parser.parse_with_db()

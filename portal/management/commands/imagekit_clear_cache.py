from django.core.management.base import BaseCommand, CommandError


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
        from imagekit.utils import get_cache

        cache = get_cache()
        cache.clear()

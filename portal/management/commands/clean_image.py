from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import portal.models as models


# $ python3 manage.py clean_image recrod artist --delete

class Command(BaseCommand):
    def add_arguments(self, parser):
        print('Command', 'add_arguments')

        # Positional arguments
        parser.add_argument('models', nargs='+', type=str, help='recrod artist')

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete files instead of print them.',
        )

    def handle(self, *args, **options):
        print('Command', 'handle', args, options)

        delete = options['delete']

        for model in options['models']:
            try:
                if model == 'recrod':
                    Command.handle_clean_recrod(delete)
                elif model == 'artist':
                    Command.handle_clean_artist(delete)
            except Exception as e:
                raise CommandError('Exception "%s" has except.' % e)

            self.stdout.write(self.style.SUCCESS('Successfully clean model "%s"' % model))

    @staticmethod
    def handle_clean_recrod(delete):
        dirname_root = 'record'

        for file in os.listdir(os.path.join(settings.MEDIA_ROOT, dirname_root)):
            path_rel_record = os.path.join(dirname_root, file)
            path_abs_record = os.path.join(settings.MEDIA_ROOT, path_rel_record)

            for file in os.listdir(path_abs_record):
                path_rel_file = os.path.join(path_rel_record, file)
                path_abs_file = os.path.join(settings.MEDIA_ROOT, path_rel_file)

                def path_exists(path_rel_file):
                    try:
                        record_cover = models.RecordCover.objects.get(image=path_rel_file)
                        if record_cover:
                            return True
                    except models.RecordCover.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

                    try:
                        record_image_set = models.RecordImages.objects.filter(image=path_rel_file)
                        if record_image_set:
                            return True
                    except models.RecordImages.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

                    return False

                if not path_exists(path_rel_file):
                    print('file to delete:', path_rel_file)
                    if delete:
                        os.remove(path_abs_file)

            if len(os.listdir(path_abs_record)) == 0:
                print('dir to delete:', path_rel_record)
                if delete:
                    os.rmdir(path_abs_record)

    @staticmethod
    def handle_clean_artist(delete):
        dirname_root = 'artist'

        for file in os.listdir(os.path.join(settings.MEDIA_ROOT, dirname_root)):
            path_rel_artist = os.path.join(dirname_root, file)
            path_abs_artist = os.path.join(settings.MEDIA_ROOT, path_rel_artist)

            for file in os.listdir(path_abs_artist):
                path_rel_file = os.path.join(path_rel_artist, file)
                path_abs_file = os.path.join(settings.MEDIA_ROOT, path_rel_file)

                def path_exists(path_rel_file):
                    try:
                        artist_avatar = models.ArtistAvatar.objects.get(image=path_rel_file)
                        if artist_avatar:
                            return True
                    except models.ArtistAvatar.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

                    try:
                        artist_image_set = models.ArtistImages.objects.filter(image=path_rel_file)
                        if artist_image_set:
                            return True
                    except models.ArtistImages.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

                    return False

                if not path_exists(path_rel_file):
                    print('file to delete:', path_rel_file)
                    if delete:
                        os.remove(path_abs_file)

            if len(os.listdir(path_abs_artist)) == 0:
                print('dir to delete:', path_rel_artist)
                if delete:
                    os.rmdir(path_abs_artist)

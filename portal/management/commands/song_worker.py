from django.core.management.base import BaseCommand, CommandError
from django.db.models import QuerySet

from portal.models import Song, SongWorker, WorkerType


class Command(BaseCommand):

    def add_arguments(self, parser):
        print('Command', 'add_arguments')
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        try:
            objects: QuerySet[Song] = Song.objects.all()
            # print('objects', objects)
            count = objects.count()
            print('objects count', count)
            for index, song in enumerate(objects):
                print('|-%s/%s' % (index + 1, count), 'song:', song)

                Command.handle_worker(1, 'composer', song, song.composer)
                Command.handle_worker(2, 'lyricist', song, song.lyricist)
                Command.handle_worker(3, 'arranger', song, song.arranger)
                Command.handle_worker(4, 'vocalist', song, song.vocalist)
                Command.handle_worker(5, 'producer', song, song.producer)

        except Exception as e:
            raise CommandError('Exception: "%s".' % e)

        self.stdout.write(
            self.style.SUCCESS('Successfully closed command "%s"' % 'song_worker')
        )

    @staticmethod
    def handle_worker(type_id, type_name, song, value):
        print(' -handle_worker():', type_id, type_name, value)
        if value:
            pass
            worker = SongWorker(song=song, type_id=type_id, name=value)
            worker.save()

            # split = value.split('/')
            # print(' -split:', type_name, split)
            #
            # # workers = SongWorker.objects.filter(song=song, type=type_id)
            # # # workers = song.songworker_set.filter(type=type_id)
            # # print(' -workers:', type_name, workers)
            #
            # for index, worker in enumerate(split):
            #     print(' -index:', index, 'worker', worker)
            #
            #     worker = SongWorker(song=song, type_id=type_id, name=worker, order=index)
            #     worker.save()

# -*- coding: utf-8 -*-
try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import portal.util as util
import portal.models as models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(settings.MEDIA_ROOT)
hf = util.HashingFiles()


class Artist():
    def __init__(self, name: str = None):
        self.name: str = name
        self.avatar = None

    def __str__(self) -> str:
        return 'Artist({} {})'.format(self.name, self.avatar)


# '/Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/歌手'
# $ python3 manage.py import_artist_image '/Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/歌手'

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
        files = os.listdir(path)
        print('files', files)
        for file in files:
            path_rel_artist_src = os.path.join(path, file)
            if os.path.isdir(path_rel_artist_src):
                path_xml = os.path.join(path_rel_artist_src, 'Artist.xml')

                if os.path.exists(path_xml):
                    print('path_xml', path_xml)
                    element_tree = etree.parse(path_xml)
                    element_root = element_tree.getroot()

                    artist = Artist()

                    for element in element_root:
                        if element.tag == 'Name':
                            artist.name = element.text
                        elif element.tag == 'Avatar':
                            for element_file in element:
                                artist.avatar = element_file.text

                    print(artist)

                    try:
                        db_artist = models.Artist.objects.get(name=artist.name)
                        print('db_artist', db_artist)

                        path_abs_artist_dst = os.path.join(settings.MEDIA_ROOT, 'artist', db_artist.dirname())
                        if not os.path.exists(path_abs_artist_dst):
                            print('path_abs_artist_dst', path_abs_artist_dst)
                            os.makedirs(path_abs_artist_dst)

                        hash_avatar = None
                        try:
                            print('db_artist.artistavatar', db_artist.artistavatar)
                            if db_artist.artistavatar:
                                hash_avatar = hf.md5_hash_large(db_artist.artistavatar.image.path)
                        except Exception as e:
                            print(e)

                        try:
                            if artist.avatar:
                                path_abs_avatar_src = os.path.join(path_rel_artist_src, artist.avatar)
                                print('path_abs_avatar_src', path_abs_avatar_src)
                                md5 = hf.md5_hash_large(path_abs_avatar_src)
                                print('md5 != hash_avatar', (md5 != hash_avatar))
                                if md5 != hash_avatar:
                                    path_abs = os.path.join('artist', db_artist.dirname(), artist.avatar)
                                    with open(path_abs_avatar_src, 'rb') as f:
                                        full_path = fs.save(path_abs, f)
                                        print('full_path', full_path)

                                        try:
                                            if db_artist.artistavatar:
                                                db_artist.artistavatar.delete()
                                        except Exception as e:
                                            print(e)

                                        db_artistavatar = models.ArtistAvatar(artist=db_artist)
                                        db_artistavatar.image.name = full_path
                                        db_artistavatar.save()

                                        # print_image_field(db_recordcover.image)
                        except Exception as e:
                            print(e)

                    except models.Artist.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

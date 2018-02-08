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
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import portal.util as util

import portal.models as models

fs = FileSystemStorage(settings.MEDIA_ROOT)
hf = util.HashingFiles()


def print_image_field(image_field):
    print('image_field', image_field)
    print('image_field', image_field.name)
    print('image_field', image_field.path)
    print('image_field', image_field.url)
    print('image_field', image_field.file)


class Record(object):
    def __init__(self):
        self.title = None
        self.number = None
        self.cover = []
        self.images = []

    def __str__(self) -> str:
        return 'Record({}, {})'.format(self.title, self.number)


# '/Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/唱片'
# $ python3 manage.py import_artist_image '/Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/唱片'

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
        for file in files:
            path_record_src = os.path.join(path, file)
            if os.path.isdir(path_record_src):
                path_xml = os.path.join(path_record_src, 'Record.xml')
                if os.path.exists(path_xml):
                    # print('path_xml', path_xml)

                    element_tree = etree.parse(path_xml)
                    element_root = element_tree.getroot()

                    record = Record()

                    for element in element_root:
                        if element.tag == 'Title':
                            record.title = element.text
                        elif element.tag == 'Number':
                            record.number = element.text
                        elif element.tag == 'Cover':
                            for element_file in element:
                                record.cover.append(element_file.text)
                        elif element.tag == 'Gallery':
                            for element_file in element:
                                record.images.append(element_file.text)

                    # print(record)

                    try:
                        db_record = models.Record.objects.get(title=record.title, number=record.number)
                        print('db_record', db_record)

                        path_record_dst = os.path.join(settings.MEDIA_ROOT, 'record', db_record.dirname())
                        if not os.path.exists(path_record_dst):
                            print('path_record_dst', path_record_dst)
                            os.makedirs(path_record_dst)

                        cover_hash_list = []
                        try:
                            if db_record.recordcover:
                                md5 = hf.md5_hash_large(db_record.recordcover.image.path)
                                cover_hash_list.append(md5)
                        except Exception as e:
                            print(e)

                        try:

                            if len(record.cover) != 0:
                                cover = record.cover[0]
                                path_abs_cover_src = os.path.join(path_record_src, cover)
                                print('path_abs_cover_src', path_abs_cover_src)
                                md5 = hf.md5_hash_large(path_abs_cover_src)
                                print('md5 not in cover_hash_list', (md5 not in cover_hash_list))
                                if md5 not in cover_hash_list:
                                    name = os.path.join('record', db_record.dirname(), cover)
                                    with open(path_abs_cover_src, 'rb') as f:
                                        full_path = fs.save(name, f)
                                        print('full_path', full_path)

                                        try:
                                            if db_record.recordcover:
                                                db_record.recordcover.delete()
                                        except Exception as e:
                                            print(e)

                                        db_recordcover = models.RecordCover(record=db_record)
                                        db_recordcover.image.name = full_path
                                        db_recordcover.save()

                                        print_image_field(db_recordcover.image)
                        except Exception as e:
                            print(e)

                        images_hash_list = []
                        try:
                            query_set = db_record.recordimages_set.all()
                            for record_image in query_set:
                                if record_image.image:
                                    md5 = hf.md5_hash_large(record_image.image.path)
                                    images_hash_list.append(md5)
                        except Exception as e:
                            print(e)

                        try:
                            if len(record.images) != 0:
                                for image in record.images:
                                    path_abs_image_src = os.path.join(path_record_src, image)
                                    print('path_abs_image_src', path_abs_image_src)
                                    md5 = hf.md5_hash_large(path_abs_image_src)
                                    print('md5 not in images_hash_list', (md5 not in images_hash_list))
                                    if md5 not in images_hash_list:
                                        name = os.path.join('record', db_record.dirname(), image)
                                        with open(path_abs_image_src, 'rb') as f:
                                            full_path = fs.save(name, f)
                                            print('full_path', full_path)

                                            db_recordimage = models.RecordImages(record=db_record)
                                            db_recordimage.image = full_path
                                            # db_recordimage.width =
                                            # db_recordimage.height =
                                            db_recordimage.save()

                                            print_image_field(db_recordimage.image)
                        except Exception as e:
                            print(e)

                    except models.Record.DoesNotExist as e:
                        pass
                    except Exception as e:
                        print(e)

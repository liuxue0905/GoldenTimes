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
import pymysql
import shutil
import portal.util as util


class Record(object):
    def __init__(self, title=None, number=None, cover=None):
        self.title = title
        self.number = number
        self.cover = cover
        self.gallery = []

    def writeXML(self, path):
        root = etree.Element("Record")

        elementTitle = etree.Element('Title')
        elementNumber = etree.Element('Number')
        elementCover = etree.Element('Cover')
        elementGallery = etree.Element('Gallery')

        elementTitle.text = self.title
        elementNumber.text = self.number

        if self.cover:
            elementFile = etree.Element('File')
            elementFile.text = self.cover
            elementCover.append(elementFile)

        for image in self.gallery:
            elementFile = etree.Element('File')
            elementFile.text = image
            elementGallery.append(elementFile)

        root.append(elementTitle)
        root.append(elementNumber)
        root.append(elementCover)
        root.append(elementGallery)

        print('root', etree.tostring(root, encoding='unicode'))

        try:
            et = etree.ElementTree(root)
            et.write(path, encoding="utf-8", method="xml", pretty_print=True, xml_declaration=True)
            return True
        except Exception as e:
            print(e)

        return False


root = '/Volumes/新加卷/我的备份/开发/流金岁月唱片库'
dirname_root_src = root
dirname_root_dst = os.path.join(root, '图片整理/唱片')

# /Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/唱片

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='',
                             db='GoldenTimes-2018',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def results_to_records(results):
    records = []

    record = None

    row_no = 0
    for row in results:
        row_no += 1
        # print('row', row_no, row)

        title = row['唱片标题']
        number = row['唱片编号']
        image_type = row['图片类型']
        image = row['图片路径']

        if record == None or (record.title != title and record.number != number):
            record = Record()
            record.title = title
            record.number = number
            records.append(record)

        if image_type == 'front':
            record.cover = image

        if image_type == 'gallery':
            record.gallery.append(image)

    # print(len(records))

    dict = {}
    for record in records:
        record_dir_name = '[{title}][{number}]'.format(title=record.title, number=record.number)
        if record_dir_name in dict:
            records.remove(record)
        else:
            dict[record_dir_name] = record

    # print(len(records))

    return records


def dirname(title, number):
    dirname = '[{title}][{number}]'.format(title=util.lx_quote(title), number=util.lx_quote(number))
    return dirname


def mkdir(root, title, number):
    path_rel_record = dirname(title, number)

    try:
        # no = 1
        # while os.path.exists(os.path.join(root, record_dir_name)):
        #     no += 1
        #     record_dir_name = '{path}({no})'.format(path=record_dir_name, no=no)
        # os.makedirs(os.path.join(root, record_dir_name))
        # return record_dir_name, os.path.join(root, record_dir_name)

        path_abs_record = os.path.join(root, path_rel_record)
        if not os.path.exists(path_abs_record):
            os.makedirs(path_abs_record)
        return path_rel_record, path_abs_record
    except Exception as e:
        print(e)

    return None, None


try:
    with connection.cursor() as cursor:
        print('cursor', cursor)

        dirname_project = os.path.dirname(os.path.dirname(__file__))
        dirname_sql = os.path.join(dirname_project, 'sql')
        filename_sql = os.path.join(dirname_sql, '唱片图片.sql')

        sql = util.get_file_content(filePath=filename_sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        records = results_to_records(results)

        print('records', records)

        for record_src in records:
            (path_rel_record_dst, path_abs_record_dst) = mkdir(dirname_root_dst, record_src.title, record_src.number)

            record_dst = Record(title=record_src.title, number=record_src.number)

            format = dirname(record_src.title, record_src.number) + '({no}){extension}'

            count = 0
            if record_src.cover:
                file_src = record_src.cover
                path_src = os.path.join(dirname_root_src, file_src)
                if os.path.exists(path_src):
                    extension = util.get_extension(record_src.cover)
                    file_dst = format.format(no=count, extension=extension)
                    record_dst.cover = file_dst

                    path_dst = os.path.join(path_abs_record_dst, file_dst)
                    print('path_src', path_src)
                    print('path_dst', path_dst)
                    dst = shutil.copy(path_src, path_dst)
                    print('dst', dst)

            for file_src in record_src.gallery:
                path_src = os.path.join(dirname_root_src, file_src)
                if os.path.exists(path_src):
                    count += 1
                    extension = util.get_extension(file_src)
                    file_dst = format.format(no=count, extension=extension)
                    record_dst.gallery.append(file_dst)

                    path_dst = os.path.join(path_abs_record_dst, file_dst)
                    print('path_src', path_src)
                    print('path_dst', path_dst)
                    dst = shutil.copy(path_src, path_dst)
                    print('dst', dst)

            path_xml = os.path.join(path_abs_record_dst, 'Record.xml')
            print('path_xml', path_xml)
            print('record_dst.writeXML()', record_dst.writeXML(path_xml))



finally:
    connection.close()

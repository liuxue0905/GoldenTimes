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


class Artist(object):
    def __init__(self, name=None):
        self.name = name
        self.avatar = None

    def writeXML(self, path):
        root = etree.Element("Artist")

        elementName = etree.Element('Name')
        elementCover = etree.Element('Avatar')

        elementName.text = self.name

        if self.avatar:
            elementFile = etree.Element('File')
            elementFile.text = self.avatar
            elementCover.append(elementFile)

        root.append(elementName)
        root.append(elementCover)

        print('root', etree.tostring(root, encoding='unicode'))

        try:
            et = etree.ElementTree(root)
            et.write(path, encoding="utf-8", method="xml", pretty_print=True, xml_declaration=True)
            return True
        except Exception as e:
            print(e)

        return False

    def __str__(self):
        return '%s %s' % (self.name, self.avatar)

    def __repr__(self):
        return self.__str__()


root = '/Volumes/新加卷/我的备份/开发/流金岁月唱片库'
dirname_root_src = root
dirname_root_dst = os.path.join(root, '图片整理/歌手')


# /Volumes/新加卷/我的备份/开发/流金岁月唱片库/图片整理/歌手

def results_to_artists(results):
    artists = []

    row_no = 0
    for row in results:
        row_no += 1
        # print('row', row_no, row)

        name = row['歌手名称']
        image_type = row['图片类型']
        image = row['图片路径']

        artist = Artist()
        artist.name = name
        artists.append(artist)

        if image_type == 'avatar':
            artist.avatar = image

    dict = {}
    for artist in artists:
        artist_dir_name = '[{name}]'.format(name=artist.name)
        if artist_dir_name in dict:
            artists.remove(artist)
        else:
            dict[artist_dir_name] = artist

    return artists


def dirname(name):
    dirname = '[{name}]'.format(name=util.lx_quote(name))
    return dirname


def mkdir(root, name):
    path_rel_artist = dirname(name)
    path_abs_artist = os.path.join(root, path_rel_artist)

    try:
        if not os.path.exists(path_abs_artist):
            os.makedirs(path_abs_artist)
        return True, path_rel_artist, path_abs_artist
    except Exception as e:
        print(e)

    return False, path_rel_artist, path_abs_artist


connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='',
                             db='GoldenTimes-2018',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        print('cursor', cursor)

        dirname_project = os.path.dirname(__file__)
        dirname_sql = os.path.join(dirname_project, 'sql')
        filename_sql = os.path.join(dirname_sql, '歌手图片.sql')

        sql = util.get_file_content(filePath=filename_sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        artists = results_to_artists(results)

        for artist_src in artists:
            (success, path_rel_artist_dst, path_abs_artist_dst) = mkdir(dirname_root_dst, artist_src.name)
            # print((success, path_rel_artist_dst, path_abs_artist_dst))

            artist_dst = Artist(name=artist_src.name)

            format = dirname(artist_src.name) + '({no}){extension}'

            count = 0
            if artist_src.avatar:
                path_src = os.path.join(dirname_root_src, artist_src.avatar)
                if os.path.exists(path_src):
                    extension = util.get_extension(artist_src.avatar)
                    file_dst = format.format(no=count, extension=extension)
                    artist_dst.avatar = file_dst

                    path_dst = os.path.join(path_abs_artist_dst, file_dst)
                    print('path_src', path_src)
                    print('path_dst', path_dst)
                    dst = shutil.copy(path_src, path_dst)
                    print('dst', dst)

            path_xml = os.path.join(path_abs_artist_dst, 'Artist.xml')
            print('path_xml', path_xml)
            print('artist_dst.writeXML()', artist_dst.writeXML(path_xml))

finally:
    connection.close()

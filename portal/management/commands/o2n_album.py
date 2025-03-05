

from django.core.management.base import BaseCommand, CommandError

import mysql.connector
import os.path
import mimetypes

from django.db.models import QuerySet
from portal.models import Record, RecordCover, RecordImages


class Command(BaseCommand):

    def add_arguments(self, parser):
        print('Command', 'add_arguments')
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):

        try:
            # 连接参数
            host = "liujinsuiyue.familyds.com"
            user = "liuxue"
            password = "LiuXue@19870905"
            # database = "golden_times"
            database = "test-liuxue"
            port = 53306

            # 建立连接
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
            )

            # Command.handle_records(conn)
            Command.handle_fronts(conn)
            Command.handle_others(conn)

            # with conn.cursor() as cursor:
            #     # 查询所有用户
            #     sql = "SELECT * FROM album_art_type;"
            #     cursor.execute(sql)
            #
            #     # 获取所有结果
            #     results = cursor.fetchall()
            #
            #     # 遍历结果并打印
            #     for row in results:
            #         print(row)

            # 关闭连接
            conn.close()
        # except Error as e:
        #     print("连接数据库失败", e)
        except Exception as e:
            self.stdout.write(
                self.style.SUCCESS('Successfully closed command "%s"' % e)
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully closed command "%s"' % 'song_worker')
        )

    @staticmethod
    def handle_records(conn):
        records: QuerySet[Record] = Record.objects.all()
        count = records.count()
        print('records count', count)
        for index, record in enumerate(records):
            print('|-%s/%s' % (index + 1, count), 'record:', record)

            album_dic = {}
            album_dic["id"] = record.id
            album_dic["title"] = record.title
            album_dic["code"] = record.number
            album_dic["year"] = record.year
            album_dic["release_date"] = record.release_detail
            album_dic["release_order"] = record.release_order
            album_dic["packaging"] = record.format
            album_dic["type"] = None
            album_dic["description"] = record.description
            print("album_dic", album_dic)

    @staticmethod
    def handle_fronts(conn):
        fronts: QuerySet[RecordCover] = RecordCover.objects.all()
        count = fronts.count()
        print('fronts count', count)

        exists_false_list = []

        for index, front in enumerate(fronts):
            print('|-%s/%s' % (index + 1, count), 'front:', front)

            cover_art_dict = {}
            # cover_art_dict["id"] = 0
            cover_art_dict["album"] = front.record_id
            cover_art_dict["image"] = front.image.name.replace('record/', '')

            (type, encoding) = mimetypes.guess_type(front.image.name)
            cover_art_dict["mime_type"] = type

            exists = os.path.exists(front.image.path)

            if not exists:
                exists_false_list.append(front.image.path)

            if front.width:
                cover_art_dict["width"] = front.width
            elif exists:
                cover_art_dict["width"] = front.image.width

            if front.width:
                cover_art_dict["height"] = front.height
            elif exists:
                cover_art_dict["height"] = front.image.height

            print("cover_art_dict", cover_art_dict)

            # cursor = conn.cursor(prepared=True)
            cursor = conn.cursor(dictionary=True)

            sql = ("SELECT * FROM album_cover_art WHERE album = %s AND image = %s LIMIT 1")
            cursor.execute(sql, (cover_art_dict["album"], cover_art_dict["image"]))
            result = cursor.fetchone()
            # (id, album, image, mimeType, width, height) = cursor.fetchone()
            # print("result", (id, album, image, mimeType, width, height))
            print("album_cover_art result", result)

            if result:
                rowid = result["id"]
                print("album_cover_art rowid 1", rowid)
                sql = "UPDATE album_cover_art SET mime_type = %s, width = %s, height = %s WHERE id = %s"
                val = (cover_art_dict["mime_type"], cover_art_dict.get("width", None), cover_art_dict.get("height", None), rowid)
                cursor.execute(sql, val)

                rowcount = cursor.rowcount
                print("album_cover_art rowcount", rowcount)
                cover_art_dict["id"] = rowid
            else:
                sql = "INSERT INTO album_cover_art (album, image, mime_type, width, height) VALUES (%s, %s, %s, %s, %s)"
                val = (cover_art_dict["album"], cover_art_dict["image"], cover_art_dict["mime_type"], cover_art_dict.get("width", None), cover_art_dict.get("height", None))
                cursor.execute(sql, val)

                rowid = cursor.lastrowid
                print("album_cover_art rowid 2", rowid)
                cover_art_dict["id"] = rowid

            cover_art_type_dict = {}
            cover_art_type_dict["id"] = cover_art_dict["id"]
            cover_art_type_dict["type_id"] = 1
            print("cover_art_type_dict", cover_art_type_dict)

            sql = ("SELECT * FROM album_cover_art_type WHERE id = %s AND type_id = %s LIMIT 1")
            cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))
            result = cursor.fetchone()
            print("album_cover_art_type result", result)

            if not result:
                sql = ("INSERT INTO album_cover_art_type (id, type_id) VALUES (%s, %s)")
                cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))

                # conn.commit()
                rowid = cursor.lastrowid
                print("album_cover_art_type rowid", rowid)

        conn.commit()

        print("exists_false_list", exists_false_list)

    @staticmethod
    def handle_others(conn):
        others: QuerySet[RecordImages] = RecordImages.objects.all()
        count = others.count()
        print('others count', count)

        exists_false_list = []

        for index, other in enumerate(others):
            print('|-%s/%s' % (index + 1, count), 'other:', other)

            cover_art_dict = {}
            # cover_art_dict["id"] = 0
            cover_art_dict["album"] = other.record_id
            cover_art_dict["image"] = other.image.name.replace('record/', '')

            (type, encoding) = mimetypes.guess_type(other.image.name)
            cover_art_dict["mime_type"] = type

            exists = os.path.exists(other.image.path)

            if not exists:
                exists_false_list.append(other.image.path)

            if other.width:
                cover_art_dict["width"] = other.width
            elif exists:
                cover_art_dict["width"] = other.image.width

            if other.width:
                cover_art_dict["height"] = other.height
            elif exists:
                cover_art_dict["height"] = other.image.height

            print("cover_art_dict", cover_art_dict)

            # cursor = conn.cursor(prepared=True)
            cursor = conn.cursor(dictionary=True)

            stmt = ("SELECT * FROM album_cover_art WHERE album = %s AND image = %s LIMIT 1")
            cursor.execute(stmt, (cover_art_dict["album"], cover_art_dict["image"]))
            result = cursor.fetchone()
            print("album_cover_art result", result)

            if result:
                rowid = result["id"]
                print("album_cover_art rowid 1", rowid)
                sql = "UPDATE album_cover_art SET mime_type = %s, width = %s, height = %s WHERE id = %s"
                val = (cover_art_dict["mime_type"], cover_art_dict.get("width", "NULL"), cover_art_dict.get("height", "NULL"), rowid)
                cursor.execute(sql, val)

                rowcount = cursor.rowcount
                print("album_cover_art rowcount", rowcount)
                cover_art_dict["id"] = rowid
            else:
                sql = "INSERT INTO album_cover_art (album, image, mime_type, width, height) VALUES (%s, %s, %s, %s, %s)"
                val = (cover_art_dict["album"], cover_art_dict["image"], cover_art_dict["mime_type"], cover_art_dict.get("width", "NULL"), cover_art_dict.get("height", "NULL"))
                cursor.execute(sql, val)

                rowid = cursor.lastrowid
                print("album_cover_art rowid 2", rowid)
                cover_art_dict["id"] = rowid

            cover_art_type_dict = {}
            cover_art_type_dict["id"] = cover_art_dict["id"]
            cover_art_type_dict["type_id"] = 3
            print("cover_art_type_dict", cover_art_type_dict)

            sql = ("SELECT * FROM album_cover_art_type WHERE id = %s AND type_id = %s LIMIT 1")
            cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))
            result = cursor.fetchone()
            print("album_cover_art_type result", result)

            if not result:
                sql = ("INSERT INTO album_cover_art_type (id, type_id) VALUES (%s, %s)")
                cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))

                # conn.commit()
                rowid = cursor.lastrowid
                print("album_cover_art_type rowid", rowid)

        conn.commit()

        print("exists_false_list", exists_false_list)

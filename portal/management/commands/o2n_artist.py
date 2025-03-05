from django.core.management.base import BaseCommand, CommandError

import mysql.connector
import os.path
import mimetypes

from django.db.models import QuerySet
from portal.models import Artist, ArtistAvatar, ArtistImages


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

            # Command.handle_artist(conn)
            Command.handle_avatar(conn)

            # with conn.cursor() as cursor:
            #     # 查询所有用户
            #     sql = "SELECT * FROM artist_art_type;"
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
        # except pymysql.Error as e:
        #     print("连接数据库失败", e)
        except Exception as e:
            self.stdout.write(
                self.style.SUCCESS('Successfully closed command "%s"' % e)
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully closed command "%s"' % 'song_worker')
        )

    @staticmethod
    def handle_artist(conn):
        artists: QuerySet[Artist] = Artist.objects.all()
        count = artists.count()
        print('artists count', count)
        for index, artist in enumerate(artists):
            print('|-%s/%s' % (index + 1, count), 'artist:', artist)

            artist_dic = {}
            artist_dic["id"] = artist.id
            artist_dic["title"] = artist.name
            artist_dic["type"] = artist.type
            print("artist_dic", artist_dic)

    @staticmethod
    def handle_avatar(conn):
        avatars: QuerySet[ArtistAvatar] = ArtistAvatar.objects.all()
        count = avatars.count()
        print('avatars count', count)
        exists_false_list = []
        for index, avatar in enumerate(avatars):
            print('|-%s/%s' % (index + 1, count), 'avatar:', avatar)

            cover_art_dict = {}
            # cover_art_dict["id"] = 0
            cover_art_dict["artist"] = avatar.artist_id
            cover_art_dict["image"] = avatar.image.name.replace('artist/', '')

            (type, encoding) = mimetypes.guess_type(avatar.image.name)
            cover_art_dict["mime_type"] = type

            exists = os.path.exists(avatar.image.path)

            if not exists:
                exists_false_list.append(avatar.image.path)

            if avatar.width:
                cover_art_dict["width"] = avatar.width
            elif exists:
                cover_art_dict["width"] = avatar.image.width

            if avatar.width:
                cover_art_dict["height"] = avatar.height
            elif exists:
                cover_art_dict["height"] = avatar.image.height

            print("cover_art_dict", cover_art_dict)

            # cursor = conn.cursor(prepared=True)
            cursor = conn.cursor()

            sql = ("SELECT * FROM artist_cover_art WHERE artist = %s AND image = %s LIMIT 1")
            cursor.execute(sql, (cover_art_dict["artist"], cover_art_dict["image"]))
            result = cursor.fetchone()
            print("artist_cover_art result", result)

            if result:
                rowid = result["id"]
                print("artist_cover_art rowid 1", rowid)
                sql = "UPDATE artist_cover_art SET mime_type = %s, width = %s, height = %s WHERE id = %s"
                val = (cover_art_dict["mime_type"], cover_art_dict.get("width", None), cover_art_dict.get("height", None), rowid)
                cursor.execute(sql, val)

                rowcount = cursor.rowcount
                print("artist_cover_art rowcount", rowcount)
                cover_art_dict["id"] = rowid
            else:
                sql = "INSERT INTO artist_cover_art (artist, image, mime_type, width, height) VALUES (%s, %s, %s, %s, %s)"
                val = (cover_art_dict["artist"], cover_art_dict["image"], cover_art_dict["mime_type"], cover_art_dict.get("width", None), cover_art_dict.get("height", None))
                cursor.execute(sql, val)

                rowid = cursor.lastrowid
                print("artist_cover_art rowid 2", rowid)
                cover_art_dict["id"] = rowid

            cover_art_type_dict = {}
            cover_art_type_dict["id"] = cover_art_dict["id"]
            cover_art_type_dict["type_id"] = 1
            print("cover_art_type_dict", cover_art_type_dict)

            sql = ("SELECT * FROM artist_cover_art_type WHERE id = %s AND type_id = %s LIMIT 1")
            cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))
            result = cursor.fetchone()
            print("artist_cover_art_type result", result)

            if not result:
                sql = ("INSERT INTO artist_cover_art_type (id, type_id) VALUES (%s, %s)")
                cursor.execute(sql, (cover_art_type_dict["id"], cover_art_type_dict["type_id"]))

                # conn.commit()
                rowid = cursor.lastrowid
                print("artist_cover_art_type rowid", rowid)

        conn.commit()

        print("exists_false_list", exists_false_list)

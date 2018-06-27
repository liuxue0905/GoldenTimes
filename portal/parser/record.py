#!python3
# coding:utf8
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import portal.parser.util as util

import logging
import logging.config
from portal.parser.logging_config import LOGGING

from portal.models import Record, Song, Artist, Company

logger = logging.getLogger('parser')


class CSVRow:
    class Record:
        title: str = None
        producer: str = None
        number: str = None
        format: str = None
        release: str = None
        release_order: str = None
        recorder: str = None
        mixer: str = None
        bandsman: str = None
        description: str = None

        company_name: str = None

        artists: str = None

        @staticmethod
        def read_from_row(row):
            record = CSVRow.Record()

            record.title = util.str_strip(row[0])
            record.producer = row[1]
            record.number = util.str_strip(row[2])
            record.format = row[3]
            record.release = row[4]
            record.release_order = row[5]
            record.recorder = row[8]
            record.mixer = row[9]
            record.bandsman = row[11]
            record.description = row[10]

            record.company_name = row[6]

            record.artists = row[7]

            return record

        def __str__(self):
            return '[{title}][{number}]'.format(title=self.title, number=self.number)

        def __repr__(self):
            return '[{title}][{number}]'.format(title=self.title, number=self.number)

    class Song:
        track: str = None
        title: str = None
        composer: str = None
        lyricist: str = None
        arranger: str = None
        bandsman: str = None
        vocalist: str = None
        producer: str = None
        description: str = None

        artists: str = None
        artists_part: str = None

        @staticmethod
        def read_from_row(row):
            song = CSVRow.Song()

            song.track = util.str_strip(row[12])
            song.title = util.str_strip(row[14])
            song.composer = row[15]
            song.lyricist = row[16]
            song.arranger = row[17]
            song.bandsman = row[18]
            song.vocalist = row[20]
            song.producer = row[21]
            song.description = row[22]

            song.artists = row[13]
            song.artists_part = row[19]

            return song

        def __str__(self):
            return '[{track}][{title}]'.format(track=self.track, title=self.title)

        def __repr__(self):
            return '[{track}][{title}]'.format(track=self.track, title=self.title)

    record: Record = None
    song: Song = None

    @staticmethod
    def read_from_row(row):
        ws_row = CSVRow()

        ws_row.record = CSVRow.Record.read_from_row(row)
        ws_row.song = CSVRow.Song.read_from_row(row)

        return ws_row


class RecordParser:
    def __init__(self, file):
        self.file = file
        self.file_log = file + '.log'

        LOGGING['handlers']['file']['filename'] = self.file_log
        logging.config.dictConfig(LOGGING)

        logger.info("[Excel]初始化")

    def parse(self):
        logger.info('[Record]处理开始')

        def check_headers(headers):
            row_headers = ['唱片标题', '唱片监制', '唱片编号', '介质', '发布时间', '发布时间排序', '唱片公司', '唱片歌手', '唱片录音', '唱片混音', '唱片说明',
                           '唱片乐手信息', '序号', '歌手', '歌名', '作曲', '作词', '编曲', '歌曲乐手信息', '歌曲合唱', '歌曲和唱', '歌曲监制', '歌曲说明']
            return set(headers) == set(row_headers)

        def should_new_record(csv_row, record):
            if record is None:
                return True
            else:
                if csv_row.record.title and csv_row.record.title != record.title:
                    return True
                elif csv_row.record.number and csv_row.record.number != record.number:
                    return True
            return False

        def _get_or_create_company(company_name):
            company_defaults = {
                'name': company_name
            }
            company = Company.objects.get_or_create(name=company_defaults['name'], defaults=company_defaults)[0]
            return company

        def _get_or_create_artist(artist_name):
            artist_defaults = {
                'name': artist_name,
            }
            artist = Artist.objects.get_or_create(name=artist_defaults['name'], defaults=artist_defaults)[0]
            return artist

        def _get_or_create_artists(artist_name_list):
            artists = []

            for artist_name in artist_name_list:
                artist = _get_or_create_artist(artist_name=artist_name)
                artists.append(artist)

            return artists

        def _save_record(csv_row):
            # Company
            company = None
            if csv_row.record.company_name:
                company = _get_or_create_company(company_name=csv_row.record.company_name)

            # Record Artists
            def xlxs_record_artist_name_list(cell):
                if cell:
                    return csv_row.record.artists.split('/')
                return None

            artist_name_list = xlxs_record_artist_name_list(csv_row.record.artists)

            artists = _get_or_create_artists(artist_name_list)

            record_defaults = {
                'title': csv_row.record.title,
                'producer': csv_row.record.producer,
                'number': csv_row.record.number,
                'format': Record.format_value_to_key(csv_row.record.format),
                'release': csv_row.record.release,
                'release_order': csv_row.record.release_order,
                'recorder': csv_row.record.recorder,
                'mixer': csv_row.record.mixer,
                'bandsman': csv_row.record.bandsman,
                'description': csv_row.record.description,
                'company': company,
            }

            obj, created = Record.objects.update_or_create(title=record_defaults['title'],
                                                           number=record_defaults['number'],
                                                           defaults=record_defaults)

            # print('record.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('record.artists', 'stop', obj.artists, obj.artists.all())

            return obj

        def _save_record_song(record, raw_song):
            logger.info(
                '[{record_title}][{record_number}] [{song_track}][{song_title}]'.format(record_title=record.title,
                                                                                        record_number=record.number,
                                                                                        song_track=raw_song.track,
                                                                                        song_title=raw_song.title))

            # Song Artists

            def xlsx_song_artist_name_list(cell_artists, cell_artists_part):
                artist_name_list = []
                if cell_artists:
                    artist_name_list += cell_artists.split('/')
                if cell_artists_part:
                    artist_name_list += cell_artists_part.split('/')
                return artist_name_list

            artist_name_list = xlsx_song_artist_name_list(raw_song.artists, raw_song.artists_part)
            # print('song artist_name_list', artist_name_list)

            artists = _get_or_create_artists(artist_name_list)

            song_defaults = {
                'track': raw_song.track,
                'title': raw_song.title,
                'composer': raw_song.composer,
                'lyricist': raw_song.lyricist,
                'arranger': raw_song.arranger,
                'bandsman': raw_song.bandsman,
                'vocalist': raw_song.vocalist,
                'producer': raw_song.producer,
                'description': raw_song.description,
            }

            obj, created = Song.objects.update_or_create(record=record, track=song_defaults['track'],
                                                         title=song_defaults['title'],
                                                         defaults=song_defaults)
            # print('song.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('song.artists', 'stop', obj.artists, obj.artists.all())

            return obj

        def _save_record_songs(record: Record, raw_songs: [CSVRow.Song]):
            # print('_save_record_songs', 'record', record)
            # print('_save_record_songs', 'raw_songs', raw_songs)

            song_set = record.song_set.all()
            # print('_save_record_songs', 'song_set', song_set)
            for song in song_set:
                def exists():
                    for raw_song in raw_songs:
                        if raw_song.track == song.track and raw_song.title == song.title:
                            return True
                    return False

                # print('_save_record_songs', 'exists', exists())
                if not exists():
                    song.delete()

            for raw_song in raw_songs:
                song = _save_record_song(record, raw_song)
                # print('_save_record_songs', 'song', song)

        try:
            with open(self.file, mode='r', newline='', encoding='utf-8-sig') as f:
                import csv
                f_csv = csv.reader(f)
                headers = next(f_csv)
                is_headers_valide = check_headers(headers)
                logger.info('[Record]标题合法: {b}'.format(b=is_headers_valide))
                if is_headers_valide:

                    record = None
                    raw_songs = None

                    record_size = 0

                    for row in f_csv:
                        # Process row
                        # print('row', row)
                        csv_row = CSVRow.read_from_row(row)
                        # print('csv_row', csv_row)

                        is_new_record = should_new_record(csv_row, record)

                        if is_new_record:
                            # 1.先保存上一条Record和Songs
                            if record and raw_songs:
                                _save_record_songs(record, raw_songs)
                            # 2.再重制Record和Songs，记录下一批
                            record_size += 1
                            logger.info('[{record_title}][{record_number}] ({count})'.format(count=record_size,
                                                                                             record_title=csv_row.record.title,
                                                                                             record_number=csv_row.record.number))
                            record = _save_record(csv_row)
                            raw_songs = []

                        raw_songs.append(csv_row.song)

                    if record and raw_songs:
                        _save_record_songs(record, raw_songs)
        except Exception as e:
            logger.info('[Record]Excption: {e}'.format(e=e))

        logger.info('[Record]处理结束')

    def parse_with_db(self):
        import os
        from django.utils import timezone

        from django.conf import settings
        from portal.models import LogImportRecord

        excel_log = LogImportRecord()
        excel_log.status = LogImportRecord.STATUS_START
        excel_log.datetime_start = timezone.now()

        try:
            excel_log.file_excel.name = os.path.relpath(self.file, os.path.abspath(settings.MEDIA_ROOT))
            excel_log.file_log.name = os.path.relpath(self.file_log, os.path.abspath(settings.MEDIA_ROOT))

            self.parse()
        except Exception as e:
            print(e)
            excel_log.status = LogImportRecord.STATUS_ERROR
        finally:
            # os.remove(filename)
            excel_log.status = LogImportRecord.STATUS_SUCCESS
            excel_log.datetime_end = timezone.now()
            excel_log.save()


def main():
    parser = RecordParser(file='/Users/liuxue/Documents/唱片.csv')
    parser.parse()
    pass


if __name__ == '__main__':
    main()

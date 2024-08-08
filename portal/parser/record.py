#!python3
# coding:utf8
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import portal.parser.util as util

import logging
import logging.config
from portal.parser.logging_config import LOGGING

from portal.models import Record, Song, Artist, Company
from portal.models import RecordWorker, SongWorker

logger = logging.getLogger('parser')

# row_headers = ['唱片标题', '唱片监制', '唱片编号', '介质', '发布时间', '发布时间排序', '唱片公司', '唱片歌手', '唱片录音', '唱片混音', '唱片说明',
#                '唱片乐手信息', '序号', '歌手', '歌名', '作曲', '作词', '编曲', '歌曲乐手信息', '歌曲合唱', '歌曲和唱', '歌曲监制', '歌曲说明']


row_headers = ['唱片标题', '唱片监制', '唱片编号', '介质', '年代', '发布时间', '发布时间排序', '唱片公司', '唱片歌手', '唱片录音', '唱片混音', '唱片说明',
               '唱片乐手信息', '序号', '歌手', '歌名', '作曲', '作词', '编曲', '歌曲乐手信息', '歌曲合唱', '歌曲和唱', '歌曲监制', '歌曲说明']


def column_index(column):
    return row_headers.index(column)


COLUMN_INDEX_RECORD_TITLE = column_index('唱片标题')  # 0
COLUMN_INDEX_RECORD_PRODUCER = column_index('唱片监制')  # 1 # D
COLUMN_INDEX_RECORD_NUMBER = column_index('唱片编号')  # 2
COLUMN_INDEX_RECORD_FORMAT = column_index('介质')  # 3
COLUMN_INDEX_RECORD_YEAR = column_index('年代')  # 4
COLUMN_INDEX_RECORD_RELEASE_DETAIL = column_index('发布时间')  # 5
COLUMN_INDEX_RECORD_RELEASE_ORDER = column_index('发布时间排序')  # 6
COLUMN_INDEX_RECORD_COMPANY = column_index('唱片公司')  # 7
COLUMN_INDEX_RECORD_ALBUM_ARTIST = column_index('唱片歌手')  # 8
COLUMN_INDEX_RECORD_RECORDER = column_index('唱片录音')  # 9 # D
COLUMN_INDEX_RECORD_MIXER = column_index('唱片混音')  # 10 # D
COLUMN_INDEX_RECORD_DESCRIPTION = column_index('唱片说明')  # 11
COLUMN_INDEX_RECORD_BANDSMAN = column_index('唱片乐手信息')  # 12

COLUMN_INDEX_SONG_TRACK = column_index('序号')  # 13
COLUMN_INDEX_SONG_ARTIST = column_index('歌手')  # 14
COLUMN_INDEX_SONG_TITLE = column_index('歌名')  # 15
COLUMN_INDEX_SONG_COMPOSER = column_index('作曲')  # 16 # D
COLUMN_INDEX_SONG_LYRICIST = column_index('作词')  # 17 # D
COLUMN_INDEX_SONG_ARRANGER = column_index('编曲')  # 18 # D
COLUMN_INDEX_SONG_BANDSMAN = column_index('歌曲乐手信息')  # 19
COLUMN_INDEX_SONG_ARTIST_PART = column_index('歌曲合唱')  # 14
COLUMN_INDEX_SONG_VOCALIST = column_index('歌曲和唱')  # 21 # D
COLUMN_INDEX_SONG_PRODUCER = column_index('歌曲监制')  # 22 # D
COLUMN_INDEX_SONG_DESCRIPTION = column_index('歌曲说明')  # 23


class CSVRow:
    class Record:
        def __init__(self):
            self.title: str = None
            self.number: str = None
            self.format: str = None
            self.year: str = None
            self.release_detail: str = None
            self.release_order: str = None
            self.bandsman: str = None
            self.description: str = None

            self.company_name: str = None

            self.artists: str = None

        @staticmethod
        def read_from_row(row):
            record = CSVRow.Record()

            record.title = util.str_strip(row[COLUMN_INDEX_RECORD_TITLE])
            record.number = util.str_strip(row[COLUMN_INDEX_RECORD_NUMBER])
            record.format = row[COLUMN_INDEX_RECORD_FORMAT]
            record.year = row[COLUMN_INDEX_RECORD_YEAR]
            record.release_detail = row[COLUMN_INDEX_RECORD_RELEASE_DETAIL]
            record.release_order = row[COLUMN_INDEX_RECORD_RELEASE_ORDER]
            record.bandsman = row[COLUMN_INDEX_RECORD_BANDSMAN]
            record.description = row[COLUMN_INDEX_RECORD_DESCRIPTION]

            record.company_name = row[COLUMN_INDEX_RECORD_COMPANY]

            record.artists = row[COLUMN_INDEX_RECORD_ALBUM_ARTIST]

            return record

        def __str__(self):
            return '[{title}][{number}]'.format(title=self.title, number=self.number)

        def __repr__(self):
            return '[{title}][{number}]'.format(title=self.title, number=self.number)

    class Song:
        def __init__(self):
            self.track: str = None
            self.title: str = None
            # self.composer: str = None
            # self.lyricist: str = None
            # self.arranger: str = None
            self.bandsman: str = None
            # self.vocalist: str = None
            # self.producer: str = None
            self.description: str = None

            self.artists: str = None
            self.artists_part: str = None

        @staticmethod
        def read_from_row(row):
            song = CSVRow.Song()

            song.track = util.str_strip(row[COLUMN_INDEX_SONG_TRACK])
            song.title = util.str_strip(row[COLUMN_INDEX_SONG_TITLE])
            # song.composer = row[COLUMN_INDEX_SONG_COMPOSER]
            # song.lyricist = row[COLUMN_INDEX_SONG_LYRICIST]
            # song.arranger = row[COLUMN_INDEX_SONG_ARRANGER]
            song.bandsman = row[COLUMN_INDEX_SONG_BANDSMAN]
            # song.vocalist = row[COLUMN_INDEX_SONG_VOCALIST]
            # song.producer = row[COLUMN_INDEX_SONG_PRODUCER]
            song.description = row[COLUMN_INDEX_SONG_DESCRIPTION]

            song.artists = row[COLUMN_INDEX_SONG_ARTIST]
            song.artists_part = row[COLUMN_INDEX_SONG_ARTIST_PART]

            return song

        def __str__(self):
            return '[{track}][{title}]'.format(track=self.track, title=self.title)

        def __repr__(self):
            return '[{track}][{title}]'.format(track=self.track, title=self.title)

    class RecordWorker:
        def __init__(self):
            self.producer: str = None
            self.recorder: str = None
            self.mixer: str = None

        @staticmethod
        def read_from_row(row):
            worker = CSVRow.RecordWorker()

            worker.producer = row[COLUMN_INDEX_RECORD_PRODUCER]
            worker.recorder = row[COLUMN_INDEX_RECORD_RECORDER]
            worker.mixer = row[COLUMN_INDEX_RECORD_MIXER]

            return worker

        def __str__(self):
            return '[{producer}][{recorder}][{mixer}]'.format(producer=self.producer, recorder=self.recorder, mixer=self.mixer)

        def __repr__(self):
            return '[{producer}][{recorder}][{mixer}]'.format(producer=self.producer, recorder=self.recorder, mixer=self.mixer)

    class SongWorker:
        def __init__(self):
            self.composer: str = None
            self.lyricist: str = None
            self.arranger: str = None
            self.vocalist: str = None
            self.producer: str = None

        @staticmethod
        def read_from_row(row):
            worker = CSVRow.SongWorker()

            worker.composer = row[COLUMN_INDEX_SONG_COMPOSER]
            worker.lyricist = row[COLUMN_INDEX_SONG_LYRICIST]
            worker.arranger = row[COLUMN_INDEX_SONG_ARRANGER]
            worker.vocalist = row[COLUMN_INDEX_SONG_VOCALIST]
            worker.producer = row[COLUMN_INDEX_SONG_PRODUCER]

            return worker

        def __str__(self):
            return '[{composer}][{lyricist}][{arranger}][{vocalist}][{producer}]'.format(composer=self.lyricist, lyricist=self.lyricist, arranger=self.arranger, vocalist=self.vocalist, producer=self.producer)

        def __repr__(self):
            return '[{composer}][{lyricist}][{arranger}][{vocalist}][{producer}]'.format(composer=self.lyricist, lyricist=self.lyricist, arranger=self.arranger, vocalist=self.vocalist, producer=self.producer)

    record: Record = None
    song: Song = None
    recordWorker: RecordWorker = None
    songWorker: SongWorker = None

    @staticmethod
    def read_from_row(row):
        ws_row = CSVRow()

        ws_row.record = CSVRow.Record.read_from_row(row)
        ws_row.song = CSVRow.Song.read_from_row(row)

        ws_row.recordWorker = CSVRow.RecordWorker.read_from_row(row)
        ws_row.songWorker = CSVRow.SongWorker.read_from_row(row)

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
                'number': csv_row.record.number,
                'format': Record.format_value_to_key(csv_row.record.format),
                'year': csv_row.record.year,
                'release_detail': csv_row.record.release_detail,
                'release_order': csv_row.record.release_order,
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

            def _save_record_worker(type_id, name):
                if worker.producer:
                    defaults = {
                        'name': name,
                    }
                    model, created = RecordWorker.objects.update_or_create(record=obj, type_id=type_id, defaults=defaults)
                    model.save()
                else:
                    RecordWorker.objects.filter(record=obj, type_id=type_id).delete()

            worker = csv_row.recordWorker
            _save_record_worker(5, worker.producer)
            _save_record_worker(6, worker.recorder)
            _save_record_worker(7, worker.mixer)

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
                'bandsman': raw_song.bandsman,
                'description': raw_song.description,
            }

            obj, created = Song.objects.update_or_create(record=record, track=song_defaults['track'],
                                                         title=song_defaults['title'],
                                                         defaults=song_defaults)
            # print('song.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('song.artists', 'stop', obj.artists, obj.artists.all())

            def _save_song_worker(type_id, name):
                if worker.producer:
                    defaults = {
                        'name': name,
                    }
                    model = SongWorker.objects.update_or_create(song=obj, type_id=type_id, defaults=defaults)
                    model.save()
                else:
                    try:
                        RecordWorker.objects.filter(record=obj, type_id=type_id).delete()
                    except Exception as e:
                        print(e)

            worker = csv_row.songWorker
            _save_song_worker(1, worker.composer)
            _save_song_worker(2, worker.lyricist)
            _save_song_worker(3, worker.arranger)
            _save_song_worker(4, worker.vocalist)
            _save_song_worker(5, worker.producer)

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
                        # print('row[0]', row[0])
                        # print('row[column_index(\'唱片标题\')]', row[column_index('唱片标题')])
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

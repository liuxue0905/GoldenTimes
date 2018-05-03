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

        def _save_record_song(record, csv_row):
            logger.info(
                '[{record_title}][{record_number}] [{song_track}][{song_title}]'.format(record_title=record.title,
                                                                                        record_number=record.number,
                                                                                        song_track=csv_row.song.track,
                                                                                        song_title=csv_row.song.title))

            # Song Artists

            def xlsx_song_artist_name_list(cell_artists, cell_artists_part):
                artist_name_list = []
                if cell_artists:
                    artist_name_list += cell_artists.split('/')
                if cell_artists_part:
                    artist_name_list += cell_artists_part.split('/')
                return artist_name_list

            artist_name_list = xlsx_song_artist_name_list(csv_row.song.artists, csv_row.song.artists_part)
            # print('song artist_name_list', artist_name_list)

            artists = _get_or_create_artists(artist_name_list)

            song_defaults = {
                'track': csv_row.song.track,
                'title': csv_row.song.title,
                'composer': csv_row.song.composer,
                'lyricist': csv_row.song.lyricist,
                'arranger': csv_row.song.arranger,
                'bandsman': csv_row.song.bandsman,
                'vocalist': csv_row.song.vocalist,
                'producer': csv_row.song.producer,
                'description': csv_row.song.description,
                'record': record
            }

            obj, created = Song.objects.update_or_create(track=song_defaults['track'], title=song_defaults['title'],
                                                         defaults=song_defaults)
            # print('song.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('song.artists', 'stop', obj.artists, obj.artists.all())

            return obj

        import csv
        with open(self.file, mode='r', newline='', encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            if check_headers(headers):

                record = None
                record_size = 0

                for row in f_csv:
                    # Process row
                    # print('row', row)
                    csv_row = CSVRow.read_from_row(row)
                    print('csv_row', csv_row)

                    if should_new_record(csv_row, record):
                        record_size += 1
                        logger.info('[{record_title}][{record_number}] ({count})'.format(count=record_size,
                                                                                         record_title=csv_row.record.title,
                                                                                         record_number=csv_row.record.number))
                        record = _save_record(csv_row)

                    _save_record_song(record, csv_row)

        logger.info('[Record]处理结束')


def main():
    parser = RecordParser(file='/Users/liuxue/Documents/唱片.csv')
    parser.parse()
    pass


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import openpyxl

from openpyxl.utils import (
    coordinate_from_string,
    column_index_from_string,
    get_column_letter,
    range_boundaries,
    rows_from_range,
    coordinate_to_tuple,
    absolute_coordinate,
)

from portal.models import Record, Song, Artist, Company

import logging
import logging.config
from portal.excel.excel_logging import LOGGING

logger = logging.getLogger('xlsx')

ws_record_titles = ['唱片标题', '唱片监制', '唱片编号', '介质', '发布时间', '发布时间排序', '唱片公司', '唱片歌手', '唱片录音', '唱片混音', '唱片说明',
                    '唱片乐手信息', '序号', '歌手', '歌名', '作曲', '作词', '编曲', '歌曲乐手信息', '歌曲合唱', '歌曲和唱', '歌曲监制', '歌曲说明']
ws_artist_titles = ['歌手姓名', '歌手类型']


def str_strip(value):
    s = str(value) if value else None
    if s:
        s = s.strip()
    return s


class ExcelParser(object):
    def __init__(self, filename_excel, filename_log):

        self.filename_excel = filename_excel
        self.filename_log = filename_log

        LOGGING['handlers']['file']['filename'] = self.filename_log
        logging.config.dictConfig(LOGGING)

        logger.info("[Excel]初始化")

    def parse(self):
        logger.info("[Excel]开始加载")
        wb = openpyxl.load_workbook(filename=self.filename_excel, read_only=True)
        logger.info("[Excel]加载完毕")

        logger.info("[Excel]工作表数量: {0}".format(len(wb.worksheets)))
        logger.info("[Excel]工作表名称: {0}".format(wb.sheetnames))

        try:
            self.parse_worksheet_record(wb.worksheets[0])
            self.parse_worksheet_artist(wb.worksheets[1])
        except Exception as e:
            logger.error("[Excel]异常错误: {0}".format(e))

            import sys, traceback

            # traceback.print_exc()

            exc_type, exc_value, exc_traceback = sys.exc_info()
            list = traceback.format_exception(exc_type, exc_value, exc_traceback)

            msg = '\r\n'
            for str in list:
                msg += str
                msg += '\r\n'

            logger.error(msg)

        finally:
            logger.info("[Excel]导入结束")

    def parse_worksheet_record(self, ws):
        logger.info('[Record]处理开始')
        logger.info("[Record]工作表名称: {0}; 最大行数: {1}; 最大列数: {2};".format(ws.title, ws.max_row, ws.max_column))

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

        def _save_record(row):
            xlsx_record_title = str_strip(row[0].value)
            xlsx_record_producer = row[1].value
            xlsx_record_number = str_strip(row[2].value)
            xlsx_record_format = row[3].value
            xlsx_record_release = row[4].value
            xlsx_record_release_order = row[5].value
            xlsx_record_recorder = row[8].value
            xlsx_record_mixer = row[9].value
            xlsx_record_bandsman = row[11].value
            xlsx_record_description = row[10].value

            xlsx_record_company_name = row[6].value

            xlsx_cell_record_artists = row[7].value

            # print('_save_record()')
            # logger.info('[{0}][{1}]'.format(xlsx_record_title, xlsx_record_number))

            # Company
            company = None
            if xlsx_record_company_name:
                company = _get_or_create_company(company_name=xlsx_record_company_name)

            # Record Artists
            def xlxs_record_artist_name_list(cell):
                if cell:
                    return xlsx_cell_record_artists.split('/')
                return None

            artist_name_list = xlxs_record_artist_name_list(xlsx_cell_record_artists)

            artists = _get_or_create_artists(artist_name_list)

            record_defaults = {
                'title': xlsx_record_title,
                'producer': row[1].value,
                'number': xlsx_record_number,
                'format': Record.format_value_to_key(row[3].value),
                'release': row[4].value,
                'release_order': row[5].value,
                'recorder': row[8].value,
                'mixer': row[9].value,
                'bandsman': row[11].value,
                'description': row[10].value,
                'company': company,
            }

            obj, created = Record.objects.update_or_create(title=record_defaults['title'],
                                                           number=record_defaults['number'],
                                                           defaults=record_defaults)

            # print('record.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('record.artists', 'stop', obj.artists, obj.artists.all())

            return obj

        def _save_record_song(record, row):
            xlxs_song_track = str_strip(row[12].value)
            xlxs_song_title = str_strip(row[14].value)
            xlxs_song_composer = row[15].value
            xlxs_song_lyricist = row[16].value
            xlxs_song_arranger = row[17].value
            xlxs_song_bandsman = row[18].value
            xlxs_song_vocalist = row[20].value
            xlxs_song_producer = row[21].value
            xlxs_song_description = row[22].value

            xlsx_song_artists = row[13].value
            xlsx_song_artists_part = row[19].value

            logger.info(
                '[{record_title}][{record_number}] [{song_track}][{song_title}]'.format(record_title=record.title,
                                                                                        record_number=record.number,
                                                                                        song_track=xlxs_song_track,
                                                                                        song_title=xlxs_song_title))

            # Song Artists

            def xlsx_song_artist_name_list(cell_artists, cell_artists_part):
                artist_name_list = []
                if cell_artists:
                    artist_name_list += cell_artists.split('/')
                if cell_artists_part:
                    artist_name_list += cell_artists_part.split('/')
                return artist_name_list

            artist_name_list = xlsx_song_artist_name_list(xlsx_song_artists, xlsx_song_artists_part)
            # print('song artist_name_list', artist_name_list)

            artists = _get_or_create_artists(artist_name_list)

            song_defaults = {
                'track': xlxs_song_track,
                'title': xlxs_song_title,
                'composer': row[15].value,
                'lyricist': row[16].value,
                'arranger': row[17].value,
                'bandsman': row[18].value,
                'vocalist': row[20].value,
                'producer': row[21].value,
                'description': row[22].value,
                'record': record
            }

            obj, created = Song.objects.update_or_create(track=song_defaults['track'], title=song_defaults['title'],
                                                         defaults=song_defaults)
            # print('song.artists', 'start', obj.artists, obj.artists.all())
            obj.artists.set(artists)
            # print('song.artists', 'stop', obj.artists, obj.artists.all())

            return obj

        # def get_merged_cell_ranges_a(merged_cell_ranges):
        #     range_string_a = []
        #
        #     for range_string in merged_cell_ranges:
        #         min_col, min_row, max_col, max_row = range_boundaries(range_string.upper())
        #         if get_column_letter(min_col) == get_column_letter(max_col) == 'A':
        #             range_string_a.append(range_string)
        #
        #     return range_string_a

        # def is_range_string_start(range_string, cell):
        #     range = range_string.split(':')
        #     if cell.coordinate == range[0]:
        #         return True
        #     return False

        # def get_range_string(merged_cell_ranges, cell):
        #     # print('get_range_string')
        #     # print(('cell', 'coordinate', 'row', 'column', 'col_idx'),
        #     #       (cell, cell.coordinate, cell.row, cell.column, cell.col_idx))
        #     for range_string in merged_cell_ranges:
        #         # print('get_range_string', 'range_boundaries(range_string.upper()', range_boundaries(range_string.upper()))
        #         min_col, min_row, max_col, max_row = range_boundaries(range_string.upper())
        #
        #         if cell.col_idx == min_col == max_col:
        #             if min_row <= cell.row <= max_row:
        #                 return range_string
        #
        #     return None

        # def get_record_count(ws, merged_cell_ranges_a):
        #     count = 0
        #
        #     count += len(merged_cell_ranges_a)
        #
        #     ws_rows = iter(ws.rows)
        #     next(ws_rows)
        #     for row in ws_rows:
        #         col0 = row[0]
        #         range_string = get_range_string(merged_cell_ranges_a, col0)
        #         if not range_string:
        #             count += 1
        #
        #     return count

        ws_rows = iter(ws.rows)
        row0 = next(ws_rows)

        if not (row0[0].value == ws_record_titles[0] and row0[1].value == ws_record_titles[1] and row0[22].value ==
            ws_record_titles[22]):
            return

        # merged_cell_ranges_a = get_merged_cell_ranges_a(ws.merged_cell_ranges)
        # record_count = get_record_count(ws, merged_cell_ranges_a)
        # logger.info('专辑数量: {0}'.format(record_count))

        record = None
        record_size = 0

        for row in ws_rows:
            col0 = row[0]
            # print(('col0', 'coordinate', 'row', 'column', 'col_idx'),
            #       (col0, col0.coordinate, col0.row, col0.column, col0.col_idx))

            xlsx_record_title = str_strip(row[0].value)
            xlsx_record_producer = row[1].value
            xlsx_record_number = str_strip(row[2].value)
            xlsx_record_format = row[3].value
            xlsx_record_release = row[4].value
            xlsx_record_release_order = row[5].value
            xlsx_record_recorder = row[8].value
            xlsx_record_mixer = row[9].value
            xlsx_record_bandsman = row[11].value
            xlsx_record_description = row[10].value
            xlxs_song_track = row[12].value
            xlxs_song_title = row[14].value
            xlxs_song_composer = row[15].value
            xlxs_song_lyricist = row[16].value
            xlxs_song_arranger = row[17].value
            xlxs_song_bandsman = row[18].value
            xlxs_song_vocalist = row[20].value
            xlxs_song_producer = row[21].value
            xlxs_song_description = row[22].value
            xlsx_song_artists = row[13].value
            xlsx_song_artists_part = row[19].value

            # range_string = get_range_string(merged_cell_ranges_a, col0)
            #
            # if not range_string or is_range_string_start(range_string, col0):
            #     record_size += 1
            #     logger.debug('正在处理: {0}/{1} {2}'.format(record_size, record_count, xlsx_record_title))
            #     record = _save_record(row)


            def should_new_record():
                if record is None:
                    return True
                else:
                    if xlsx_record_title and xlsx_record_title and xlsx_record_title != record.title:
                        return True
                    elif xlsx_record_number and xlsx_record_number and xlsx_record_number != record.number:
                        return True
                return False

            if should_new_record():
                record_size += 1
                logger.info('[{record_title}][{record_number}] ({count})'.format(count=record_size,
                                                                                 record_title=xlsx_record_title,
                                                                                 record_number=xlsx_record_number))
                record = _save_record(row)

            _save_record_song(record=record, row=row)

        logger.info('[Record]处理结束')

    def parse_worksheet_artist(self, ws):
        logger.info('[Artist]处理开始')
        logger.info("[Artist]工作表名称: {0}; 最大行数: {1}; 最大列数: {2};".format(ws.title, ws.max_row, ws.max_column))

        ws_rows = iter(ws.rows)
        row0 = next(ws_rows, None)

        if not (row0[0].value == ws_artist_titles[0] and row0[1].value == ws_artist_titles[1]):
            return

        artist_count = ws.max_row - 1
        logger.info('[Artist]歌手数量: {0}'.format(artist_count))

        for row in ws_rows:
            xlsx_name = row[0].value
            xlsx_type = row[1].value

            # print(('col0', 'coordinate', 'row', 'column', 'col_idx'),
            #       (col0, col0.coordinate, col0.row, col0.column, col0.col_idx))

            artist_defaults = {
                'name': xlsx_name,
                'type': Artist.type_value_to_key(xlsx_type)
            }

            Artist.objects.update_or_create(name=artist_defaults['name'], defaults=artist_defaults)

        logger.info('[Artist]处理结束')

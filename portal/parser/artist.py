# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import portal.parser.util as util

import logging
import logging.config
from portal.parser.logging_config import LOGGING

from portal.models import Artist

logger = logging.getLogger('parser')


class CSVRow:
    name: str = None
    type: str = None

    @staticmethod
    def read_from_row(row):
        csv_row = CSVRow()

        csv_row.name = util.str_strip(row[0])
        csv_row.type = util.str_strip(row[1])

        return csv_row


class ArtistParser:
    def __init__(self, file):
        self.file = file
        self.file_log = file + '.log'

        LOGGING['handlers']['file']['filename'] = self.file_log
        logging.config.dictConfig(LOGGING)

        logger.info("[Excel]初始化")

    def parse(self):
        logger.info('[Artist]处理开始')

        def check_headers(headers):
            row_headers = ['歌手姓名', '歌手类型']
            return set(headers) == set(row_headers)

        import csv
        with open(self.file, mode='r', newline='', encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            print('headers', headers)
            if check_headers(headers):
                for row in f_csv:
                    # Process row
                    # print('row', row)
                    csv_row = CSVRow.read_from_row(row)
                    print('csv_row', csv_row)

                    artist_defaults = {
                        'name': csv_row.name,
                        'type': Artist.type_value_to_key(csv_row.type)
                    }

                    Artist.objects.update_or_create(name=artist_defaults['name'], defaults=artist_defaults)

        logger.info('[Artist]处理结束')


def main():
    parser = ArtistParser(file='/Users/liuxue/Documents/歌手.csv')
    parser.parse()
    pass


if __name__ == '__main__':
    main()

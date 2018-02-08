# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib.parse import quote_plus, unquote_plus


def get_file_content(filePath):
    """ 读取图片 """
    with open(filePath, 'rb') as fp:
        return fp.read()


windows = '"*/:<>?\|'


def lx_quote(string):
    from io import StringIO
    result = StringIO()

    for char in string:
        if char in windows:
            quote = quote_plus(char)
            result.write(quote)
        else:
            result.write(char)

    return result.getvalue()


def lx_unquote(string: str):
    for char in windows:
        string = string.replace(quote_plus(char), char)
    return string


def get_extension(url):
    from mimetypes import MimeTypes
    mime_types = MimeTypes()

    (type, encoding) = mime_types.guess_type(url)
    extensions = mime_types.guess_all_extensions(type)
    extension = extensions[-1]

    return extension


def strftime():
    from datetime import datetime
    # (dt, micro) = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
    (dt, micro) = datetime.utcnow().strftime('%Y-%m-%d %H%M%S.%f').split('.')
    dt = "%s.%03d" % (dt, int(micro) / 1000)
    print(dt)
    return dt


class HashingFiles(object):
    def md5_hash_small(self, file):
        import hashlib

        hasher = hashlib.md5()
        # with open('myfile.jpg', 'rb') as afile:
        with open(file, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        # print(hasher.hexdigest())
        return hasher.hexdigest()

    def md5_hash_large(self, file):
        import hashlib
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        # with open('anotherfile.txt', 'rb') as afile:
        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        # print(hasher.hexdigest())
        return hasher.hexdigest()

    def sha1_hash_large(self, file):
        import hashlib
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        # with open('anotherfile.txt', 'rb') as afile:
        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        # print(hasher.hexdigest())
        return hasher.hexdigest()

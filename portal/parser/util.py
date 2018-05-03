# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def str_strip(value):
    s = str(value) if value else None
    if s:
        s = s.strip()
    return s

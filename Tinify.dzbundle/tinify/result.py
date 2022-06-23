# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from . import ResultMeta

class Result(ResultMeta):
    def __init__(self, meta, data):
        ResultMeta.__init__(self, meta)
        self.data = data

    def to_file(self, path):
        if hasattr(path, 'write'):
            path.write(self.data)
        else:
            with open(path, 'wb') as f:
                f.write(self.data)

    def to_buffer(self):
        return self.data

    @property
    def size(self):
        value = self._meta.get('Content-Length')
        return value and int(value)

    @property
    def media_type(self):
        return self._meta.get('Content-Type')

    @property
    def content_type(self):
        return self.media_type

    @property
    def location(self):
        return None

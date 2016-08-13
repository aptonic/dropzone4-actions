# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class ResultMeta(object):
    def __init__(self, meta):
        self._meta = meta

    @property
    def width(self):
        return int(self._meta['Image-Width'])

    @property
    def height(self):
        return int(self._meta['Image-Height'])

    @property
    def location(self):
        return self._meta['Location']

    def __len__(self):
        return self.size

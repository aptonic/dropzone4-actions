# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class ResultMeta(object):
    def __init__(self, meta):
        self._meta = meta

    @property
    def width(self):
        value = self._meta.get('Image-Width')
        return value and int(value)

    @property
    def height(self):
        value = self._meta.get('Image-Height')
        return value and int(value)

    @property
    def location(self):
        return self._meta.get('Location')

    def __len__(self):
        return self.size or 0

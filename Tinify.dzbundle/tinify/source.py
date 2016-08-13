# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import tinify
from . import Result, ResultMeta

class Source(object):
    @classmethod
    def from_file(cls, path):
        if hasattr(path, 'read'):
            return cls._shrink(path)
        else:
            with open(path, 'rb') as f:
                return cls._shrink(f.read())

    @classmethod
    def from_buffer(cls, string):
        return cls._shrink(string)

    @classmethod
    def from_url(cls, url):
        return cls._shrink({"source": {"url": url}})

    @classmethod
    def _shrink(cls, obj):
        response = tinify.get_client().request('POST', '/shrink', obj)
        return cls(response.headers.get('location'))

    def __init__(self, url, **commands):
        self.url = url
        self.commands = commands

    def preserve(self, *options):
        return type(self)(self.url, **self._merge_commands(preserve=self._flatten(options)))

    def resize(self, **options):
        return type(self)(self.url, **self._merge_commands(resize=options))

    def store(self, **options):
        response = tinify.get_client().request('POST', self.url, self._merge_commands(store=options))
        return ResultMeta(response.headers)

    def result(self):
        response = tinify.get_client().request('GET', self.url, self.commands)
        return Result(response.headers, response.content)

    def to_file(self, path):
        return self.result().to_file(path)

    def to_buffer(self):
        return self.result().to_buffer()

    def _merge_commands(self, **options):
        commands = self.commands.copy()
        commands.update(options)
        return commands

    def _flatten(self, items, seqtypes=(list, tuple)):
        items = list(items)
        for i, x in enumerate(items):
            while isinstance(items[i], seqtypes):
                items[i:i+1] = items[i]
        return items

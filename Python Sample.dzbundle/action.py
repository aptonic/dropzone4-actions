#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-04-30

import sys
import time

import dropzone as dz

if __name__ == '__main__':
    action = sys.argv[1]
    items = sys.argv[2:]

    dz.begin("Started! Action: %s, %d items" % (action, len(items)))
    time.sleep(1)
    dz.determinate(True)
    dz.percent(30)
    time.sleep(2)
    dz.percent(60)

    print dz.inputbox('title', 'Hello')

    time.sleep(2)
    dz.percent(80)
    time.sleep(2)
    dz.determinate(False)
    time.sleep(1)
    dz.url('http://google.com')

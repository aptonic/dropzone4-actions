#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-04-29


import os
import sys
import subprocess

def send_output(line):
    if isinstance(line, unicode):
        line = line.encode('utf8')
    sys.stdout.write(line.replace('\n', "[;n") + '\n')
    sys.stdout.flush()
    return raw_input()

def read_clipboard():
    return subprocess.check_output(["pbpaste", ])

def replace_dialog(arg):
    os.chdir(os.environ["runner_path"])
    return subprocess.check_output(["./ReplaceDialog.app/Contents/MacOS/ReplaceDialog", arg])

def cocoa_dialog(args):
    os.chdir(os.environ["runner_path"])
    return subprocess.check_output(["./CocoaDialog", ] + args)

def inputbox(title, prompt_text, field_name="Filename"):
    output = cocoa_dialog(['inputbox', '--button1', 'OK',
                           '--button2', 'Cancel',
                           '--title', title.encode('utf8'),
                           '--e', '--informative-text', prompt_text.encode('utf8')])
    button, _, input_ = output.strip().partition("\n")
    if button == "2":
        fail("Cancelled")
    if not input_:
        fail("%s cannot be empty" % field_name)
    return input_

def save_value(value_name, value):
    send_output("Save_Value_Name: %s" % value_name)
    send_output("Save_Value: %s" % value)

def temp_folder():
    folder = os.environ["support_folder"] + "/Temp"
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder

def text(t):
    send_output("Text: %s" % (t if t else "0"))

def url(url, title=None):
    if title:
        send_output("URL_Title: %s" % title)
    send_output("URL: %s" % (url if url else "0"))

def percent(value):
    send_output("Progress: %s" % str(value))

def error(title, msg):
    send_output("Error_Title: %s" % title)
    send_output("Error: %s" % msg)
    sys.exit(0)

def alert(title, msg):
    send_output("Alert_Title: %s" % title)
    send_output("Alert: %s" % msg)

def fail(msg):
    send_output("Fail: %s" % msg)
    sys.exit(0)

def finish(msg):
    send_output("Finish_Message: %s" % msg)

def begin(msg):
    send_output("Begin_Message: %s" % msg)

def determinate(value):
    send_output("Determinate: %s" % ("1" if value else "0"))

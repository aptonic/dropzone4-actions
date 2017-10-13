# Dropzone Action Info
# Name: Tinify
# Description: https://tinypng.com/
# Handles: Files
# Creator: ghui
# URL: http://ghui.me
# Events: Dragged, Clicked
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# UniqueID 100300
# MinDropzoneVersion: 3.5
# PythonPath: /usr/local/bin/python3
# LoginTitle: Tinify Config
# OptionsNIB: APIKey

import time
import os
import tinify


SUFFIX_KEY = "suffix"
HAS_SHOWED = "has_showed"
###############################################################

def dragged():
    tinify.key = read_value('api_key')
    suffix = get_suffix()
    print("1st suffix: " + suffix)
    upload_and_compress_images(items, suffix)

######################################################################

def get_suffix():
    suffix = read_value(SUFFIX_KEY).strip()
    has_showed = read_value(HAS_SHOWED)
    if (not suffix) and (not has_showed): #First time show Warning dialog
        suffix = show_set_suffix_dialog()
    if suffix == 'nil':
        suffix = ''
    return suffix


def upload_and_compress_images(paths, suffix):
    for index, path in enumerate(paths):
        name = os.path.basename(path)
        valid = check_img_is_valid(name)
        if valid:
            # do upload
            dz.determinate(False)
            progress = "(" + repr(index + 1) + "/" + repr(len(paths)) + ") "
            dz.begin(progress + "Compressing: " + name + " ...")
            source_img = tinify.from_file(path)
            if suffix:
                path = rename(path, suffix)
            source_img.to_file(path)
            compressed_name = os.path.basename(path)
            dz.finish("Image: " + name + " Compressed -> " + compressed_name)
            dz.url(False)

def rename(full_path, append_text):
    dir = os.path.dirname(full_path)
    name = os.path.basename(full_path)
    array = os.path.splitext(name)
    new_name = array[0] + append_text + array[1]
    new_path = dir + "/" + new_name
    return new_path
    
def check_img_is_valid(img_name):
    if not img_name.endswith(".png") and not img_name.endswith(".jpg"):
        return False
    return True

######################################################################
def clicked():
    show_set_suffix_dialog()

def show_set_suffix_dialog():
    save_value(HAS_SHOWED, True)
    original_suffix = read_value(SUFFIX_KEY)
    output = dz.cocoa_dialog('standard-inputbox --title "Set suffix for the compressed image" --informative-text "Enter Suffix:" --float --text ' + original_suffix)
    button, input_value = output.splitlines()
    button = button.strip().decode('utf-8')
    input_value = input_value.strip().decode('utf-8')
    if not input_value:
        input_value = 'nil'
    print('input value: ' + input_value)
    print('button : ' + button)
    if button == '1':
        save_value(SUFFIX_KEY, input_value)
    return input_value

def save_value(key, value):
    dz.save_value(key, value)

def read_value(key):
    try:
        value = os.environ[key]
    except:
        value = ''
    if key == SUFFIX_KEY:
        if value == 'nil':
            value = ''
    return value


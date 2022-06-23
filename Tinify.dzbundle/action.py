# Dropzone Action Info
# Name: Tinify
# Description: Greatly reduces PNG, JPEG or WEBP file sizes using the\nhttps://tinypng.com API.\n\nYou can get an API key at https://tinypng.com/developers
# Handles: Files
# Creator: Aptonic
# URL: https://aptonic.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# UniqueID 100300
# MinDropzoneVersion: 4.0
# OptionsNIB: APIKey
# OptionsTitle: Tinify Config

import time
import os
import tinify

def dragged():
    tinify.key = os.environ["api_key"]
    upload_and_compress_images(items)

def upload_and_compress_images(paths):
    if not check_img_types_valid(paths):
        dz.fail("You must drag PNG, JPG or WEBP files to convert")
    
    dz.determinate(False)
    output_paths = []
    
    for index, path in enumerate(paths):
        # Use Tinify API to compress dragged image
        name = os.path.basename(path)
        progress = "(" + repr(index + 1) + "/" + repr(len(paths)) + ") "
        dz.begin(progress + "Compressing: " + name + "...")
        source_img = tinify.from_file(path)
        destination_path = rename(path, "-1")
        source_img.to_file(destination_path)
        if os.path.exists(destination_path):
            output_paths.append(destination_path)
        
    s = "s" if len(items) > 1 else ""
        
    if len(output_paths) == len(items):
        dz.finish("Image" + s + " Successfully Compressed")
        dz.url(False)
    else:
        dz.fail("Image" + s + " Failed to Compress")
    

def rename(full_path, append_text):
    dir = os.path.dirname(full_path)
    name = os.path.basename(full_path)
    array = os.path.splitext(name)
    new_name = array[0] + append_text + array[1]
    new_path = dir + "/" + new_name
    return new_path
    
def check_img_types_valid(paths):
    for path in paths:
        name = os.path.basename(path).lower()
        if not name.endswith(".png") and not name.endswith(".jpg") and not name.endswith(".webp"):
            return False
    return True
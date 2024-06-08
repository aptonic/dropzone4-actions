# Dropzone Action Info
# Name: Tinify
# Description: Greatly reduces PNG, JPEG or WEBP file sizes using the\nhttps://tinypng.com API.\n\nYou can get a free API key at https://tinypng.com/developers
# Handles: Files
# Creator: Aptonic
# URL: https://aptonic.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.5
# UniqueID: 100300
# MinDropzoneVersion: 4.7.6
# OptionsNIB: Tinify
# OptionsTitle: Tinify Config

import os
import tinify

def dragged():
    dz.determinate(False)

    if not check_img_types_valid(items):
        dz.fail("You must drag PNG, JPG or WEBP files to convert")

    tinify.key = os.environ["api_key"]

    if os.environ.get('output_folder_option') is None:
        if os.environ.get('sandboxed') is None:
            # Unsandboxed can just output to same folder
            os.environ["output_folder_option"] = "0"
        else:
            # Sandboxed needs to ask user where to save
            os.environ["output_folder_option"] = "1"

    if os.environ["output_folder_option"] == "0":
        # Use the same folder as the source
        output_folder = os.path.dirname(items[0])
    elif os.environ["output_folder_option"] == "1":
        # Ask the user where to save the output
        output_folder = dz.select_folder("Choose a folder to save the converted image%s to." % ("s" if len(items) > 1 else ""))
        if (output_folder == "0"):
            dz.fail("You must select an output folder")
    elif os.environ["output_folder_option"] == "2":
        # Use preselected output folder
        output_folder = os.environ["path"]

    upload_and_compress_images(items, output_folder)

def upload_and_compress_images(paths, output_folder):

    output_paths = []
    
    for index, path in enumerate(paths):
        # Use Tinify API to compress dragged image
        name = os.path.basename(path)
        progress = "(" + repr(index + 1) + "/" + repr(len(paths)) + ") "
        dz.begin(progress + "Compressing: " + name + "...")
        source_img = tinify.from_file(path)

        destination_path = output_folder + "/" + name

        # Destination path exists then add a suffix
        if os.path.exists(destination_path):
            destination_path = add_suffix(destination_path)

        source_img.to_file(destination_path)
        if os.path.exists(destination_path):
            output_paths.append(destination_path)
        
    s = "s" if len(items) > 1 else ""
        
    if len(output_paths) == len(items):
        dz.finish("Image" + s + " Successfully Compressed")
        dz.url(False)
    else:
        dz.fail("Image" + s + " Failed to Compress")

def add_suffix(full_path):
    dir = os.path.dirname(full_path)
    name = os.path.basename(full_path)
    base, ext = os.path.splitext(name)
    counter = 1
    new_name = base + "-" + str(counter) + ext
    new_path = os.path.join(dir, new_name)
    
    while os.path.exists(new_path):
        counter += 1
        new_name = base + "-" + str(counter) + ext
        new_path = os.path.join(dir, new_name)
    
    return new_path

def check_img_types_valid(paths):
    valid_extensions = [".png", ".jpg", ".jpeg", ".webp"]
    for path in paths:
        name = os.path.basename(path).lower()
        if not any(name.endswith(ext) for ext in valid_extensions):
            return False
    return True
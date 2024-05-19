# Dropzone Action Info
# Name: WeTransfer
# Description: Allows you to upload files to WeTransfer.
# Handles: Files
# Creator: Aptonic
# URL: https://aptonic.com
# Events: Clicked, Dragged
# SkipConfig: Yes
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 4.0
# UniqueID: 1038

from WeTransferTool import We
import os

def dragged():
    dz.begin(f"Uploading...")
    dz.determinate(False)

    wet = We()
    url_list = []

    for item in items:
        filename = os.path.basename(item)
        dz.begin(f"Uploading {filename}...")
        metadata = wet.upload(item, filename, 'Shared with Dropzone 4')
        url_list.append(metadata['shortened_url'])
    
    if len(url_list) > 1:
        dz.finish("URLs now on clipboard")
        dz.text('\n'.join(url_list))
    else:
        dz.finish("URL is now on clipboard")
        dz.url('\n'.join(url_list))


def clicked():
    os.system("open https://wetransfer.com/")

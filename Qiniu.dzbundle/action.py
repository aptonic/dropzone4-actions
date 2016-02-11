# Dropzone Action Info
# Name: Qiniu
# Description: Upload images to qiniu.com
# Handles: Files
# Creator: Su Yan
# URL: http://yansu.org
# OptionsNIB: ExtendedLogin
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.2
# UniqueID: 0830
# MinDropzoneVersion: 3.5

import os
import sys
import commands
import shutil
import imghdr
import webbrowser
from qiniu import Auth
from qiniu import put_file
from qiniu import BucketManager

reload(sys)
sys.setdefaultencoding('utf8')
query = None
def getAuth():
    global query
    if query != None:
        return query
    access_key = os.environ['username']
    secret_key = os.environ['password']
    query = Auth(access_key, secret_key)
    return query

def isFileExist(file_name):
    q = getAuth()
    # check if file already exist
    bucket_name = os.environ['server']
    bucket = BucketManager(getAuth())
    ret, info = bucket.stat(bucket_name, file_name)
    if ret != None:
        return True
    else:
        return False

def uploadFile(file_path, file_name):
    q = getAuth()
    bucket_name = os.environ['server']

    if isFileExist(file_name):
        dz.fail("Filename already exist")

    token = q.upload_token(bucket_name, file_name)
    ret, info = put_file(token, file_name, file_path)

    if info.status_code == 200:
        bucket_domain = os.environ.get('root_url', '')
        base_url = 'http://%s/%s' % (bucket_domain, file_name)

        # copy file to local path as backup
        if 'remote_path' in os.environ:
            dest_path = '%s/%s' % (os.environ['remote_path'], file_name)
            shutil.copyfile(file_path, dest_path)

        return base_url
    else:
        return False

def dragged():
    dz.begin("Starting uploading...")
    dz.determinate(True)
    dz.percent(10)
    
    # keep origin name
    file_path = items[0]
    file_name = os.path.basename(file_path)
    base_url  = uploadFile(file_path, file_name)

    if base_url:
        dz.finish("Upload Completed")
        dz.percent(100)
        dz.url(base_url)
    else:
        dz.fail("Upload Failed")
        dz.percent(100)
        dz.url(False)
 
def clicked():
    dz.percent(10)

    file_path = dz.temp_folder() + '/qiniu_img_cache'
    current_path = os.path.dirname(os.path.realpath(__file__))
    command = '"%s/pngpaste" "%s"' % (current_path, file_path)
    status, output = commands.getstatusoutput(command)
    if (status != 0):
        webbrowser.open("https://portal.qiniu.com/bucket/" + os.environ['server'] + "/resource")
        dz.fail(output)

    file_name = dz.inputbox("Filename Required", "Enter filename without suffix:")
    file_name = file_name + '.' + imghdr.what(file_path)

    while True:
        if isFileExist(file_name):
            file_name = dz.inputbox("Filename already exist", "Enter filename without suffix:")
            file_name = file_name + '.' + imghdr.what(file_path)
        else:
            break

    dest_path = '%s/%s' % (os.path.dirname(file_path), file_name)
    shutil.move(file_path, dest_path)

    dz.begin("Starting uploading...")
    dz.determinate(True)

    base_url = uploadFile(dest_path, file_name)
    if (base_url):
        dz.finish("Upload Completed")
        dz.percent(100)
        dz.url(base_url)
    else:
        dz.fail("Upload Failed")
        dz.percent(100)
        dz.url(False)

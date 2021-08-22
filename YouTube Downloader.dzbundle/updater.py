from urllib.request import urlretrieve
import urllib.request
import traceback
import hashlib
import json
import tarfile
import os
import shutil
import re
import utils

def update_youtubedl():
    current_version = get_yt_downloader_version()
    UPDATE_URL = 'https://rg3.github.io/youtube-dl/update/'
    VERSION_URL = UPDATE_URL + 'LATEST_VERSION'
    JSON_URL = UPDATE_URL + 'versions.json'
    
    # Check if there is a new version
    try:
        newversion = urllib.request.urlopen(VERSION_URL).read().decode('utf-8').strip()
    except Exception:
        print(traceback.format_exc())
        print('ERROR: can\'t find the current version. Please try again later.')
        return
    if newversion == current_version:
        print('youtube-dl is up-to-date (v' + current_version + ')')
        return
    
    try:
        versions_info = urllib.request.urlopen(JSON_URL).read().decode('utf-8')
        versions_info = json.loads(versions_info)
    except Exception:
        print(traceback.format_exc())
        print('ERROR: Could not download versions.json. Please try again later.')
        return
        
    print('Attempting to update youtube-dl') 

    version_id = versions_info['latest']
    
    print('Updating to version ' + version_id + ' ...')
    version = versions_info['versions'][version_id]
    
    filename = "update.tar.gz"
    
    dz.begin("Updating YouTube downloader...")
    utils.set_determinate_progress(False)
    
    try:
        os.remove(filename)
    except OSError:
        pass
    
    try:
        shutil.rmtree('yt-tmp')
    except Exception:
        pass
    
    try:
        def reporthook(blocknum, blocksize, totalsize):
            percent = int(blocknum * blocksize * 1e2 / totalsize)
            if percent > 0 and percent <= 100:
                utils.set_determinate_progress(True)
                utils.set_progress_percent(percent)
        
        urlretrieve(version['tar'][0], filename, reporthook)
        
    except Exception:
        print(traceback.format_exc())
        print('ERROR: unable to download latest version')
        return

    with open(filename, 'rb') as updatefile:
        newcontent = updatefile.read()

    newcontent_hash = hashlib.sha256(newcontent).hexdigest()
    if newcontent_hash != version['tar'][1]:
        print('ERROR: the downloaded file hash does not match. Aborting.')
        return

    os.mkdir('yt-tmp');
        
    tar = tarfile.open(filename)
    tar.extractall("./yt-tmp")
    tar.close()
    
    # Sanity check - does downloaded youtube-dl contain an __init.py__
    check_path = 'yt-tmp/youtube-dl/youtube_dl/__init__.py'
    if os.path.exists(check_path):
        print('Extracted update looks good.')
    else:
        print(check_path + ' could not be found. Aborting update.')
        return
    
    # Delete existing library and move new one into place
    shutil.rmtree('youtube-dl')
    shutil.move('yt-tmp/youtube-dl', 'youtube-dl')
    shutil.rmtree('yt-tmp')
    os.remove('update.tar.gz')
    
    # Get new version from youtube_dl, we can't reload all youtube_dl dependencies so we will do actual download in another python instance
    old_version = current_version
    new_version = get_yt_downloader_version()
    print('Successfully updated youtube-dl library version from ' + old_version + ' to ' + new_version)
    
    
def get_yt_downloader_version():
    VERSIONFILE = 'youtube-dl/youtube_dl/version.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

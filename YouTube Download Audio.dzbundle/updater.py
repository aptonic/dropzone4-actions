try:
    from urllib.request import urlretrieve
    import urllib.request
except ImportError:
    # Python 2 fallback
    import urllib
    import urllib2
    
import traceback
import hashlib
import json
import tarfile
import os
import shutil
import re
import utils
import sys

def update_youtubedl():
    current_version = get_yt_downloader_version()
    VERSION_JSON_URL = 'https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest'
    
    python_version = sys.version_info[0]
    
    # Check if there is a new version
    try:
        if python_version == 3:
            versions_result = urllib.request.urlopen(VERSION_JSON_URL).read().decode('utf-8').strip()
        else:
            versions_result = urllib2.urlopen(VERSION_JSON_URL).read().decode('utf-8').strip()
        versions_info = json.loads(versions_result)
    except Exception:
        print(traceback.format_exc())
        print('ERROR: Could not download latest version info. Please try again later.')
        return
    
    version_id = versions_info['tag_name']
    print(f'Latest version: {version_id}, Current version: {current_version}')
    if version_tuple(current_version) >= version_tuple(version_id):
        print(f'yt-dlp is up to date ({current_version})')
        return
    
    version_download_url = (get_version(versions_info))['browser_download_url']
    
    print('Updating to version ' + version_id + ' ...')
    
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
        
        if python_version == 3:
            urlretrieve(version_download_url, filename, reporthook)
        else:
            urllib.urlretrieve(version_download_url, filename, reporthook)
        
    except Exception:
        print(traceback.format_exc())
        print('ERROR: unable to download latest version')
        return

    with open(filename, 'rb') as updatefile:
        newcontent = updatefile.read()

    newcontent_hash = hashlib.sha256(newcontent).hexdigest()
    if newcontent_hash != get_sha256sum(versions_info):
        print('ERROR: the downloaded file hash does not match. Aborting.')
        return

    os.mkdir('yt-dlp-tmp');
        
    tar = tarfile.open(filename)
    tar.extractall("./yt-dlp-tmp")
    tar.close()
    
    # Sanity check - does downloaded yt-dlp contain an __init.py__
    check_path = 'yt-dlp-tmp/yt-dlp/yt_dlp/__init__.py'
    if os.path.exists(check_path):
        print('Extracted update looks good.')
    else:
        print(check_path + ' could not be found. Aborting update.')
        return
    
    # Delete existing library and move new one into place
    shutil.rmtree('yt-dlp')
    shutil.move('yt-dlp-tmp/yt-dlp', 'yt-dlp')
    shutil.rmtree('yt-dlp-tmp')
    os.remove('update.tar.gz')
    
    # Get new version from youtube_dl, we can't reload all youtube_dl dependencies so we will do actual download in another python instance
    old_version = current_version
    new_version = get_yt_downloader_version()
    print('Successfully updated yt-dlp library version from ' + old_version + ' to ' + new_version)
    
def version_tuple(version_str):
    return tuple(map(int, version_str.split('.')))

def get_version(version_info):
    return next(i for i in version_info['assets'] if i['name'] == 'yt-dlp.tar.gz')

def get_sha256sum(version_info):
    python_version = sys.version_info[0]
    filename = 'yt-dlp.tar.gz'
    urlh = next(
        (i for i in version_info['assets'] if i['name'] in ('SHA2-256SUMS')),
        {}).get('browser_download_url')
    if not urlh:
        return None
        
    try:
        if python_version == 3:
            hash_data = urllib.request.urlopen(urlh).read().decode('utf-8')
        else:
            hash_data = urllib2.urlopen(urlh).read().decode('utf-8')
    except Exception:
        print(traceback.format_exc())
        print('ERROR: Could not download hash info. Please try again later.')
        return None
        
    return dict(ln.split()[::-1] for ln in hash_data.splitlines()).get(filename)

def get_yt_downloader_version():
    VERSIONFILE = 'yt-dlp/yt_dlp/version.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

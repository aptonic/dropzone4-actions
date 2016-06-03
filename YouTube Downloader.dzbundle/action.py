# Dropzone Action Info
# Name: YouTube Downloader
# Description: Allows you to quickly download videos from YouTube and many other video sites. Downloaded videos are placed in the selected folder.\n\nDownloads the highest quality version of the video and audio possible - This means the video and audio are sometimes downloaded seperately and the two files are automatically merged back together after the download completes.\n\nDrag a video URL onto the action or copy a URL onto the clipboard and then click the action to initiate download.
# Handles: Text
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ChooseFolder
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.3
# MinDropzoneVersion: 3.5
# UniqueID: 1036

from __future__ import unicode_literals
import sys
import updater
import os
import traceback
import re

def dragged():
    download_url(items[0])

def clicked():
    url = dz.read_clipboard()
    download_url(url)

def download_url(url):
    regex = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not regex.match(url):
        dz.fail("Not a valid video URL")
    
    dz.begin("Checking youtube-dl library is up to date...")
    dz.determinate(False)

    updater.update_youtubedl()
    
    dz.begin("Preparing to download video...")
    dz.determinate(False)

    # Put ffmpeg in PATH for merging videos audio and video
    os.environ["PATH"] += os.pathsep + os.path.join(os.getcwd(), 'ffmpeg')
    
    # Download URL from clipboard
    sys.path.append("youtube-dl")
    import youtube_dl
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(os.environ['EXTRA_PATH'], '%(title)s.%(ext)s'),
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }

    dz.determinate(True)
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(traceback.format_exc())
        dz.error("Video Download Failed", "Downloading video failed with the error:\n\n" + e.message)
        
    dz.finish("Video Download Complete")
    dz.url(False)
        

class MyLogger(object):
    def debug(self, msg):
        try:    
            print(msg)
        except Exception:
            pass

    def warning(self, msg):
        try:    
            print(msg)
        except Exception:
            pass

    def error(self, msg):
        try:    
            print(msg)
        except Exception:
            pass

def my_hook(d):
    if d['status'] == 'downloading':
        dz.begin("Downloading " + os.path.basename(d['filename']) + "...")
        dz.percent(100 * d['downloaded_bytes'] / d['total_bytes'])
    
    if d['status'] == 'finished':
        print('Download complete')

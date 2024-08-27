# Dropzone Action Info
# Name: YouTube Downloader
# Description: Allows you to download videos from YouTube and many other video sites. Downloaded videos are placed in the chosen folder.\n\nYou can convert downloaded videos to H.264 by checking the box below which will make them playable with QuickTime, but this will add extra time after the download.\n\nYou can drag a video URL onto the action or copy a URL onto the clipboard and then click the action to initiate download.
# Handles: Text
# Creator: Aptonic
# URL: https://aptonic.com
# OptionsNIB: VideoDownloader
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 3.2
# MinDropzoneVersion: 3.5
# UniqueID: 1036

from __future__ import unicode_literals
import sys
import updater
import os
import traceback
import re
import utils
import pexpect

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
    utils.set_determinate_progress(False)

    updater.update_youtubedl()
    
    dz.begin("Preparing to download video...")
    utils.set_determinate_progress(False)
    utils.reset_progress()
    
    # Put ffmpeg in PATH for merging videos audio and video
    if 'apple_silicon' in os.environ:
        os.environ["PATH"] += os.pathsep + os.path.join(os.getcwd(), 'ffmpeg-arm')
    else:
        os.environ["PATH"] += os.pathsep + os.path.join(os.getcwd(), 'ffmpeg')
    
    # Download URL from clipboard
    sys.path.append("yt-dlp")

    from yt_dlp import YoutubeDL
    
    # Store the value of the environment variable in a variable
    convert_h264 = os.environ.get("convert_h264") == "1"

    # Set the suffix based on the variable
    suffix = "_original" if convert_h264 else ""

    ydl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(os.environ['EXTRA_PATH'], f'%(title)s{suffix}.%(ext)s'),
        'logger': MyLogger(),
        'extractor_args': {'youtube': {'player_client': 'mediaconnect'}},
        'progress_hooks': [my_hook],
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            result = ydl.extract_info(url, download=True)
            final_filepath = ydl.prepare_filename(result)

    except Exception as e:
        print(traceback.format_exc())
        dz.error("Video Download Failed", "Downloading video failed with the error:\n\n" + e.message)
        
    if convert_h264:
        convert_video(final_filepath)
    
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

def convert_video(filepath):

    def time_to_seconds(time_str):
        h, m, s = map(float, time_str.split(':'))
        return h * 3600 + m * 60 + s

    output_path = os.path.join(os.environ['EXTRA_PATH'], os.path.basename(filepath).replace('_original', ''))
    launchcmd = 'ffmpeg'
    args = [
        '-i', filepath, '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k', '-y', '-movflags', '+faststart', output_path
    ]

    filename = os.path.basename(filepath)

    # Start the conversion process using pexpect
    child = pexpect.spawn(launchcmd, args, timeout=None)

    duration = None
    current_time = None

    while True:
        try:
            child.expect(['\r', '\n'])
            output = child.before.decode('utf-8')

            # Extract the duration if available
            if "Duration:" in output:
                match = re.search(r'Duration: (\d{2}:\d{2}:\d{2}\.\d{2})', output)
                if match:
                    duration = match.group(1)
                    duration_seconds = time_to_seconds(duration)
                    print(f"Video Duration is {duration}")
                    utils.set_determinate_progress(True)

            # Extract the current time progress if available
            time_match = re.search(r'time=(\d{2}:\d{2}:\d{2}\.\d{2})', output)
            if time_match:
                current_time = time_match.group(1)
                current_time_seconds = time_to_seconds(current_time)

                # Calculate the percentage of conversion completed
                if duration_seconds > 0:
                    converted_percent = int((current_time_seconds / duration_seconds) * 100)
                    print(f"Current Conversion Time is {current_time} ({converted_percent:.2f}% complete)")
                    dz.begin(f"Converting {filename} to H264, {current_time} / {duration}...")
                    dz.percent(converted_percent)

        except pexpect.EOF:
            break

    child.wait()

    # Check if the conversion was successful
    if child.exitstatus == 0:
        os.remove(filepath)
        print(f"Conversion successful, original file removed: {filepath}")
    else:
        print(f"Conversion failed with return code {child.exitstatus}")

def my_hook(d):
    if d['status'] == 'downloading':
        speed_info = ""
        
        if 'filename' in d:
            filename = os.path.basename(d['filename'])
        else:
            filename = ""
    
        if '_eta_str' in d and '_speed_str' in d:
            speed_info = " (" + d['_speed_str'] + " ETA: " + d['_eta_str'] + ")"
        filename = filename.encode('ascii', 'ignore').decode('ascii')
        dz.begin("Downloading " + filename + speed_info + "...")
        
        if '_percent_str' in d and d.get('fragment_index', 0) > 0:
            p = d['_percent_str']
            p = p.replace('%','').strip()
            progress = int(float(p))
            
            if progress <= 100:
                utils.set_determinate_progress(True)
                utils.set_progress_percent(progress)
            else:
                utils.set_determinate_progress(False)
                utils.reset_progress()
    
    if d['status'] == 'finished':
        utils.set_determinate_progress(False)
        utils.reset_progress()
        print('Download complete')

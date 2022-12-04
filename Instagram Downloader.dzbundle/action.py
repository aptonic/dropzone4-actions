# Dropzone Action Info
# Name: Instagram Downloader
# Description: Allows you to download images and videos from Instagram.\n\nDrag an Instagram post URL onto this action or right-click the URL and then choose 'Run Dropzone Action' from the services menu to use this action.\n\nProvide your Instagram login details and choose a path below to save downloaded images/videos.
# Handles: Text
# Creator: Aptonic
# URL: https://aptonic.com
# Events: Dragged
# OptionsNIB: InstagramDownloader
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.1
# MinDropzoneVersion: 4.4.4
# UniqueID: 1020

import os
import re
from datetime import datetime
import instaloader
from instaloader import Instaloader, Post
import os.path


def dragged():
    m = re.search("instagram.com/p/(.*)", items[0])

    if m is None:
        dz.error("Invalid Instagram Post URL", "The URL was not valid. You must use this action with a URL like https://www.instagram.com/p/post")
    
    dz.begin("Logging in to Instagram...")
    dz.determinate(False)

    L = instaloader.Instaloader()

    if os.path.isfile('session'):
        L.load_session_from_file(os.environ['username'], filename='session')
        
    try:
        if L.test_login() == None:
            L.login(os.environ['username'], os.environ['password'])
            L.save_session_to_file('session')
    except Exception as e:
        L.login(os.environ['username'], os.environ['password'])
        L.save_session_to_file('session')

    dz.begin("Downloading Instagram post...")

    os.chdir(os.environ['path'])

    post = Post.from_shortcode(L.context, m.group(1))
    
    filename = post.pcaption.strip('. ')
    suffix = 1
    
    while os.path.isfile(filename + ".jpg") or os.path.isfile(filename + ".jpeg"):
        filename = post.pcaption.strip('. ') + "-" + str(suffix)
        suffix += 1
        
    video_tmp_path = "tmp_video_post"
    
    if not post.is_video:
        L.download_pic(filename, post.url, datetime.now())
    else:  
        L.download_post(post, video_tmp_path)
        
    if post.is_video:
        for file in os.listdir(video_tmp_path):
            if not file.endswith(".mp4"):
                os.remove(video_tmp_path + "/" + file)
            else:
                os.replace(video_tmp_path + "/" + file, filename + ".mp4")
        os.rmdir(video_tmp_path)
    
    dz.finish("Download Complete")
    dz.url(False)

# Dropzone Action Info
# Name: YouTube
# Description: Uploads dragged videos to YouTube. \n\nYou can select the privacy level and after upload it opens the edit page of the video in the default browser.
# Handles: Files
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/youtube.upload
# Events: Dragged, Clicked
# RunsSandboxed: No
# Version: 1.5
# UniqueID: 1026
# MinDropzoneVersion: 3.2.1
# RubyPath: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/bin/ruby

require 'youtube'

def dragged
  youtube = Youtube.new

  $dz.determinate(false)

  youtube.configure_client

  $items.each do |file|
    privacy_status = youtube.read_privacy_status
    youtube.upload_video(file, privacy_status)
  end

  $dz.finish('Video(s) were uploaded to YouTube!')
  $dz.url(false)

end

def clicked
  system('open https://youtube.com')
end

# Dropzone Action Info
# Name: YouTube Uploader
# Description: Uploads dragged videos to YouTube. \n\nYou can select the privacy level and after upload it opens the edit page of the video in the default browser.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/youtube.upload
# Events: Dragged, Clicked
# RunsSandboxed: Yes
# Version: 2.2
# UniqueID: 1026
# MinDropzoneVersion: 3.2.1

require 'youtube'

def dragged
  youtube = Youtube.new

  $dz.determinate(false)

  youtube.configure_client
  privacy_status = youtube.read_privacy_status

  $items.each do |file|
    youtube.upload_video(file, privacy_status)
  end

  $dz.finish('Video(s) were uploaded to YouTube!')
  $dz.url(false)

end

def clicked
  system('open https://youtube.com')
end

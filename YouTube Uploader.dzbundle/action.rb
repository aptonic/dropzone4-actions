# Dropzone Action Info
# Name: YouTube Uploader
# Description: Uploads dragged videos to YouTube. \n\nYou can select the privacy level and after upload it opens the edit page of the video in the default browser.\n\nBy using this action you agree YouTube Terms of Service at\n https://www.youtube.com/t/terms and the Google privacy policy at https://policies.google.com/privacy\n\nYou can manage or revoke Dropzone's access to your Google Account at https://security.google.com/settings/security/permissions
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/youtube.upload
# Events: Dragged, Clicked
# RunsSandboxed: Yes
# Version: 2.7
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

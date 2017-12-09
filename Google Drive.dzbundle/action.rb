# Dropzone Action Info
# Name: Google Drive
# Description: Uploads files to Google Drive.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/drive
# Events: Dragged, Clicked
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 2.0
# MinDropzoneVersion: 3.2.1
# UniqueID: 1020

require 'gdrive'

def dragged
  gdrive = Gdrive.new

  $dz.determinate(false)

  gdrive.configure_client

  folder_id = gdrive.select_folder

  $items.each do |file|
    gdrive.upload_file(file, folder_id)
  end

  $dz.finish('File(s) were uploaded to Google Drive!')
  $dz.url(false)

end

def clicked
  system('open https://drive.google.com')
end

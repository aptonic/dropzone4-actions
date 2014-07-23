# Dropzone Action Info
# Name: SCP Upload
# Description: Allows files to be uploaded to a remote SSH server. If the option key is held down then files are zipped up before uploading.
# Handles: Files
# Events: Dragged, TestConnection
# KeyModifiers: Option
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ExtendedLogin
# DefaultPort: 22
# Version: 1.1
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1009

require 'scp_uploader'

$host_info = {:server    => ENV['server'],
              :port      => ENV['port'],
              :username  => ENV['username'],
              :password  => ENV['password']}

def dragged
  delete_zip = false
  
  if ENV['KEY_MODIFIERS'] == "Option"
    # Zip up files before uploading
    if $items.length == 1
      # Use directory or file name as zip file name
      dir_name = $items[0].split(File::SEPARATOR)[-1]
      file = ZipFiles.zip($items, "#{dir_name}.zip")
    else
      file = ZipFiles.zip($items, "files.zip")
    end
    
    # Remove quotes
    items = file[1..-2]
    delete_zip = true
  else
    # Recursive upload      
    items = $items
  end
  
  $dz.begin("Starting transfer...")
  $dz.determinate(false)

  remote_paths = SCPUploader.do_upload(items, ENV['remote_path'], $host_info)
  ZipFiles.delete_zip(items) if delete_zip
  
  # Put URL of uploaded file on pasteboard
  finish_text = "Upload Complete"
  
  if remote_paths.length == 1
    filename = remote_paths[0].split(File::SEPARATOR)[-1].strip[0..-2]
    
    if ENV['root_url'] != nil
      slash = (ENV['root_url'][-1,1] == "/" ? "" : "/")
      url = ENV['root_url'] + slash + filename
      finish_text = "URL is now on clipboard"
    else
      url = filename
    end
  else
    url = false
  end
  
  $dz.finish(finish_text)
  $dz.url(url)
end

def test_connection
  SCPUploader.test_connection($host_info)
end

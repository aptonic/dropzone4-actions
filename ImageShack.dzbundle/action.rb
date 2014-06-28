# Dropzone Action Info
# Name: ImageShack
# Description: Uploads images to ImageShack. Drop multiple images to create an album.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ImageShack
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.2
# MinDropzoneVersion: 3.0

require 'imageshack'
require 'curl_uploader'

UPLOAD_URL = "https://api.imageshack.com/v2/images"

def dragged
  imageshack = ImageShack.new
  
  $dz.determinate(false)
  
  allowed_exts = ["jpg", "jpeg", "gif", "tif", "tiff", "png", "bmp"]
  
  # Check only supported types were dragged
  $items.each do |item|
    filename = File.basename(item)
    ext = File.extname(item).downcase[1..-1]  
    $dz.fail("Only image files are supported") if not allowed_exts.include?(ext)
  end

  album_name = get_album_name if $items.length > 1
  
  auth_token = imageshack.get_auth_token(ENV['username'], ENV['password'])
  if not auth_token
    $dz.fail(imageshack.error_message)
  end
  
  uploader = CurlUploader.new
  uploader.upload_url = "https://api.imageshack.com/v2/images"
  uploader.post_vars = {:api_key => ENV['api_key'], :auth_token => auth_token}

  if $items.length == 1
    # Just do the upload and put URL on clipboard
    uploader.file_field_name = "file"
    result = uploader.upload($items)[0]
    puts result.inspect
    check_upload_output_valid(result)
    url = imageshack.get_url(result[:output])
    
    if url
      finish(url)
    else
      $dz.fail(imageshack.error_message)
    end
  else
    # Create album, upload to it then put album URL on clipboard
    album_info = imageshack.create_album(album_name, auth_token)
    uploader.file_field_name = "files"
    uploader.post_vars[:album] = album_info["result"]["id"]
    results = uploader.upload($items)
    puts results.inspect
    
    results.each do |result|
      check_upload_output_valid(result)
    end
    
    finish("https://imageshack.com/a/#{album_info["result"]["id"]}", "Album:: #{album_name}")
  end
end

def check_upload_output_valid(result)
  json_result = result[:output]
  if result[:curl_output_valid]
    return true
  else
    error_message = json_result
    $dz.fail("Invalid response. Check the debug console.")
  end
end

def get_album_name
  # Prompt for album name with CocoaDialog
  output = $dz.cocoa_dialog("inputbox --button1 \"OK\" --button2 \"Cancel\" --title \"Upload #{$items.length} Images to ImageShack\" --e --informative-text \"Enter album name:\"")
  button, album_name = output.split("\n")

  if album_name == nil
    $dz.fail("Invalid Album Name")
  end

  if button == "2"
    $dz.fail("Cancelled")
  else
    return album_name
  end
end

def finish(url, title=nil)
  $dz.finish("URL is now on clipboard")
  $dz.url(url, title)
end

def clicked
  system("open https://imageshack.com/my/images")
end

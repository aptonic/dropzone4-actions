# Dropzone Action Info
# Name: ImageShack
# Description: Uploads an image to ImageShack.
# Handles: Files
# Events: Clicked, Dragged
# KeyModifiers: Option
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ImageShack
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

require "imageshack"

FF_USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6"
UPLOAD_URL = "https://api.imageshack.com/v2/images"

def dragged
  imageshack = ImageShack.new
  
  $dz.determinate(false)
  
  file_path = $items[0]
  filename = File.basename(file_path)
  
  allowed_exts = ["jpg", "jpeg", "gif", "tif", "tiff", "png", "bmp"]
  ext = File.extname(file_path).downcase[1..-1]
  
  if not allowed_exts.include?(ext)
    $dz.fail("Not an Image")
  end
  
  $dz.begin("Uploading #{filename}...")
  
  last_output = 0
  is_receiving_json = false
  json_output = ""
  ext = "jpeg" if ext == "jpg"
  ext = "tiff" if ext == "tif"
  
  auth_token = imageshack.get_auth_token(ENV['username'], ENV['password'])
  if not auth_token
    $dz.fail(imageshack.error_message)
  end
  
  $dz.determinate(true)
  
  file_path = file_path.gsub('"', '\"')
  IO.popen("/usr/bin/curl -# -A '#{FF_USERAGENT}' -F 'api_key=#{ENV['api_key']}' -F 'auth_token=#{auth_token}' -F \"file=@#{file_path}\" #{UPLOAD_URL} 2>&1 | tr -u \"\r\" \"\n\"") do |f|
    while line = f.gets do
      if line =~ /%/ and not is_receiving_json
        line_split = line.split(" ")
        file_percent_raw = line_split[1]
        if file_percent_raw != nil
          file_percent = file_percent_raw.to_i
          if last_output != file_percent
            $dz.percent(file_percent) 
            $dz.determinate(false) if file_percent == 100
          end
          last_output = file_percent
        end
      end
      if line =~ /"success"/ or is_receiving_json
        is_receiving_json = true
        json_output += line
      else
        handle_errors(line)
      end
    end
  end
  
  url = imageshack.get_url(json_output)
  
  if url
    $dz.finish("URL is now on clipboard")
    $dz.url(url)
  else
    $dz.finish(imageshack.error_message)
    $dz.url(false)
  end
end

def handle_errors(line)
  if line[0..4] == "curl:"
    if line[6..-1] =~ /Couldn't resolve/
      $dz.error("ImageShack Upload Error", "Please check your network connection.")
    else
      $dz.error("ImageShack Upload Error", line[6..-1])
    end
  end
end

def clicked
  system("open https://imageshack.com/my/images")
end

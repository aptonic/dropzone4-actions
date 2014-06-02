# Dropzone Action Info
# Name: Desktop Picture
# Description: A dropped image will be set as the current desktop background. Hello
# Handles: Files
# Events: Dragged
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.2
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1002

def dragged
  $dz.determinate(false)
  
  file_path = $items[0]
  file_name = File.basename(file_path)
  
  $dz.begin("Changing to #{file_name}...")
  
  allowed_exts = ["jpg", "jpeg", "gif", "tif", "tiff", "png", "bmp"]
  ext = File.extname(file_path).downcase[1..-1]
  
  if allowed_exts.include?(ext)
    %x(osascript -e 'tell application "System Events" to set picture of current desktop to "#{file_path}"' >& /dev/null)
    $dz.finish("Desktop Changed")
  else
    $dz.finish("Not an Image")
  end
  
  $dz.url(false)
end

# Dropzone Action Info
# Name: Edit Images in Pixelmator Pro
# Description: Dropped images will be opened in Pixelmator Pro.
# Handles: Files
# Creator: Sachin Shekhar
# URL: https://sachinshekhar.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  allowed_exts = ["jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp", "psd", "svg", "pdf", "webp", "tga"]
  
  supported_files = $items.select {|item| allowed_exts.include?(File.extname(item).downcase[1..-1])}
  
  # Open all supported files in Pixelmator Pro
  if !supported_files.empty?
    supported_files.each do |file|
      system("open", "-a", "Pixelmator Pro", file)
    end
  end
  
  # Notify about unsupported files
  unsupported_files = $items - supported_files
  $dz.fail(unsupported_files.length.to_s + " unsupported file#{'s' if unsupported_files.length > 1} not opened:\n\n" + unsupported_files.join("\n\n")) if !unsupported_files.empty?
end

def clicked
  system("open", "-a", "Pixelmator Pro")
end

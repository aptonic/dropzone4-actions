# Dropzone Action Info
# Name: 1024px
# Description: Resize all images to a maximum width of 1024 pixels.  Uses built in Mac Commands.  No prerequisites to install.
# Handles: Files
# Events: Dragged
# Creator: Maverick Stoklosa
# URL: http://github.com/maverick2000/dropzone3_resize_1024px
# SkipConfig: Yes
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueId: 1014

def dragged
  standard_types = ["jpg", "jpeg", "png"]
  $dz.begin("Running task...")
  $dz.determinate(true)
  num = 0
  $items.each do |item|
    extension = File.extname(item).downcase[1..-1]
    if standard_types.include?(extension)
      `sips -Z 1024 \"#{item}\" 2>&1`
    else
      $dz.error("Error", "Only JPG and PNG supported.")
    end
    num += 1
    $dz.percent((num.to_f/$items.length)*100.0)
  end
  $dz.finish("Resizing complete")
  $dz.url(false)
end

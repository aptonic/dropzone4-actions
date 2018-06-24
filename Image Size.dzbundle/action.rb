# Dropzone Action Info
# Name: Image Size
# Description: Displays the width and height of a local or remote image file.
# Handles: Files
# Creator: Kolja Nolte
# URL: https://www.koljanolte.com
# Events: Dragged
# KeyModifiers:
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0.0
# MinDropzoneVersion: 3.0

require 'fastimage'
require 'net/http'
require 'net/https'
require 'open-uri'

def dragged
  puts $items.inspect

  $dz.begin('Analyzing file ' + File.basename($items[0]) + '...')
  $dz.determinate(true)

  $dz.percent(10)
  sleep(0.5)
  $dz.percent(50)
  sleep(0.5)
  $dz.percent(100)

  image_path   = $items[0]
  image_size   = FastImage.size(image_path)
  image_width  = image_size[0].to_s
  image_height = image_size[1].to_s
  dimensions   = image_width + 'x' + image_height
  output       = dimensions

  $dz.finish(output)

  $dz.text(dimensions)
end
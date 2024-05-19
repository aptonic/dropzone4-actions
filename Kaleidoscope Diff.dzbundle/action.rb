# Dropzone Action Info
# Name: Kaleidoscope Diff
# Description: Drag two or more files to diff them with Kaleidoscope
# Handles: Files
# Events: Dragged
# Creator: Justin Hileman
# URL: http://justinhileman.com
# Version: 1.1
# SkipConfig: Yes
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1018

def dragged
  unless system('open', '-bcom.blackpixel.kaleidoscope', *$items)
    $dz.fail('Error opening Kaleidoscope')
  end

  $dz.url(false)
end

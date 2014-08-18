# Dropzone Action Info
# Name: Kaleidoscope Diff
# Description: Drag two or more files to diff them with Kaleidoscope
# Handles: Files
# Events: Dragged
# Creator: Justin Hileman
# URL: http://justinhileman.com
# Version: 1.0
# SkipConfig: Yes
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1018

def dragged
  if $items.size < 2
    $dz.fail('Drag at least two files :)')
  end

  unless system('open', '-bcom.blackpixel.kaleidoscope', *$items)
    $dz.fail('Error opening Kaleidoscope')
  end

  $dz.url(false)
end

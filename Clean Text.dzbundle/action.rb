# Dropzone Action Info
# Name: Clean Text
# Description: Removes any formatting and puts cleaned text into clipboard. A click cleans the clipboard's contents.
# Handles: Text
# Creator: Dennis Kuypers
# URL: http://yoursite.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  $dz.text($items[0])
end
 
def clicked
  $dz.text($dz.read_clipboard)
end

# Yes, that's all.
# Dropzone Action Info
# Name: Add to SideNotes
# Description: Creates a new note in SideNotes
# Handles: Files, Text
# Creator: Apptorium
# URL: https://www.apptorium.com/sidenotes
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 3544670229

def dragged
  $dz.determinate(true)
  $dz.percent(0)

  isPathParam = ""
  if ENV['dragged_type'] == "files"
    isPathParam = "isPath YES"
  end

  for index in 0...$items.count
    item = $items[index]
    text = item.gsub('"', '\"')
    %x(osascript -e 'tell application "SideNotes" to create note text "#{text}" #{isPathParam}' >& /dev/null)
    $dz.percent(((index + 1) / $items.count) * 100)
  end

  $dz.url(false)
end
 
def clicked
  %x(osascript -e 'tell application "SideNotes" to create note text ""' >& /dev/null)
  $dz.url(false)
end

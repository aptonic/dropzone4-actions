# Dropzone Action Info
# Name: Araxis Merge
# Description: Compare files and folders via Araxis Merge (and some AppleScript)
# Handles: Files
# Creator: Stanislav Goncharov
# URL: http://git.io/gsz2Sw
# Events: Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: Yes
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0

def makeapplescript(files)
  ["tell application \"Araxis Merge\"",
   "launch",
   "compare {%s}" % (files.map { |f| "\"#{f}\"" } * ","),
   "activate",
   "end tell"]
end

def osascript(applescript)
  "osascript %s" % (applescript.map { |s| " -e '#{s}'"} * "")
end

def dragged

  $dz.begin "Comparing"
  $dz.determinate false
  
  if $items.size == 1
    $dz.fail "We can compare only two or three items. But you may stash your item into Drop Bar and compare it later"
    $dz.url false
    exit
  end
  
  script = osascript(makeapplescript($items))
  $dz.text "Try executing #{script}"
  system script
  
  if $items.size > 3
    $dz.finish "Sorry, but we compare only first three items"
  end
  
  $dz.url false
  
end


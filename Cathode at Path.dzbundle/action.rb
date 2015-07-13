# Dropzone Action Info
# Name: Cathode at Path
# Description: Drop a file or folder on this action to open a new Cathode window at the files path. You can also drop a textual path.
# Handles: Files, Text
# Creator: Nate Henry (attr. Dennis Kuypers)
# URL: https://github.com/nateski88
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 672351102879648003471169204215

def dragged
  dir = false

  case ENV['dragged_type']
  when 'files'
    # If it's a directory then cd to that directory, otherwise we will cd to the directory the file is in
    if File.directory?($items[0])
      dir = $items[0]
    else
      dir = File.dirname($items[0])
    end
  when 'text'
    # Verify that this is a directory path
    dir = $items[0] if File.directory?($items[0])
  end

  puts dir

  # Launch Cathode in desired directory
  if dir
    puts `osascript -so <<END
    tell application "Cathode"
      activate
      delay 0.5
      tell application "System Events"
        tell process "Cathode" to keystroke "n" using command down
        tell process "Cathode" to keystroke "cd '#{dir}'; clear;"
        tell process "Cathode" to keystroke return
      end
    end tell
END`
  else
    # Could not figure out what the user wants. Dump to console and notify user.
    puts "Could not figure out what to do with data: #{$items.inspect}"
    $dz.fail("Not a file or directory path")
  end

  $dz.url(false)
end

def clicked
  puts `osascript -so <<END
  tell application "Cathode"
    activate
  end tell
END`
  $dz.url(false)
end

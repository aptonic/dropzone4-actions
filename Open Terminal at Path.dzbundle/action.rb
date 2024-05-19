# Dropzone Action Info
# Name: Open Terminal at Path
# Description: Drop a file or folder on this action to open a new Terminal window at the files path. You can also drop a textual path.
# Handles: Files, Text
# Creator: Dennis Kuypers
# URL: http://dk.kymedia.de
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.2
# MinDropzoneVersion: 3.0
# UniqueID: 1030

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
    
  # Launch Terminal in desired directory
  if dir
    puts `osascript -so <<END
    tell application "Terminal"
      activate
      delay 0.2
      tell application "System Events"
        tell process "Terminal" to keystroke "t" using command down
      end
      delay 0.2
      do script "cd '#{dir}'; clear;" in selected tab of front window
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
  tell application "Terminal"
  if not (exists window 1) then reopen
    activate
  end tell
END`
  $dz.url(false)
end

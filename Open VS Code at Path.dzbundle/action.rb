# Dropzone Action Info
# Name: Open VS Code at Path
# Description: Drop a file or folder on this action to open a new VS Code window at the files path. You can also drop a textual path.
# Handles: Files, Text
# Creator: Sachin Shekhar
# URL: https://sachinshekhar.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.2
# MinDropzoneVersion: 3.0

def dragged
  dir = false
    
  case ENV['dragged_type']
  when 'files'
    # If it's a file we will use the directory the file is in
    if File.directory?($items[0])
      dir = $items[0]
    else
      dir = File.dirname($items[0])
    end
  when 'text'
    # Verify that this is a directory path
    dir = $items[0] if File.directory?($items[0])
  end
    
  # Launch VS Code in desired directory
  if dir
    puts `osascript -so <<END
    tell application "Terminal"
      activate
      delay 0.2
      tell application "System Events"
        tell process "Terminal" to keystroke "t" using command down
      end
      delay 0.2
      do script "code '#{dir}';" in selected tab of front window
      delay 5
      quit
    end tell
END`
  else
    # Could not figure out what the user wants. Dump to console and notify user.
    puts "Could not figure out what to do with data: #{$items.inspect}"
    $dz.fail("Not a file or directory path")
  end
end

def clicked
  puts `osascript -so <<END
  tell application "Code"
    activate
  end tell
END`
end

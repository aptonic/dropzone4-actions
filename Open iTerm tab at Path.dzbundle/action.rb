# Dropzone Action Info
# Name: Open iTerm tab at Path
# Description: iTerm v2.9+ required. This action uses the new Applescript used in iTerm 2.9. Drop a file or folder on this action to open a new iTerm tab at the files path. If iTerm is open but no windows exist, a new iTerm window is created. You can also drop a textual path. Slightly modified version of the "Open Terminal at Path" action by Dennis Kuypers and "Open iTerm at Path" action by Sam Turner.
# Handles: Files, Text
# Creator: Casey de la Vega-Rawson
# URL: https://github.com/caseydlvr
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 6969696969

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

  # Launch iTerm in desired directory
  if dir
    puts `osascript -so <<END
    tell application "iTerm"
      activate
      delay 0.2
      try 
        tell current window
          create tab with default profile
            tell current session
              write text "cd '#{dir}'"
            end tell
        end tell
      on error
        create window with default profile
        tell current session of current window
          write text "cd '#{dir}'"
        end tell
      end try
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
  tell application "iTerm"
    activate    
  end tell
END`
$dz.url(false)
end

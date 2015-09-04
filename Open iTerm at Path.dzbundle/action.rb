# Dropzone Action Info
# Name: Open iTerm at Path
# Description: iTerm v2.9+ required. This action uses the new Applescript used in iTerm 2.9. Drop a file or folder on this action to open a new Terminal window at the files path. You can also drop a textual path. Slightly modified version of the original action for Terminal by Dennis Kuypers.
# Handles: Files, Text
# Creator: Sam Turner
# URL: http://www.digi.ltd.uk
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# MinDropzoneVersion: 3.0


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
    set newWindow to (create window with default profile)
    delay 0.2
        tell current window
            tell current session
                write text "cd '#{dir}'"
            end tell
        end tell
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
  delay 0.2
  set newWindow to (create window with default profile )
end tell
END`
$dz.url(false)
end

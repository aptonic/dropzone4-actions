# Dropzone Action Info
# Name: Node HTTP Server at Path
# Description: Creates a Node HTTP-Server at path and opens default browser. Node http-server required, to install `npm install -g http-server` Close iTerm or CTRL+C to quit server
# Handles: Files
# Creator: Sam Turner
# URL: http://www.digi.ltd.uk
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0


def dragged
  dir = false

  $dz.begin("Starting Note HTTP Server...")
  $dz.determinate(true)

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
                write text "cd '#{dir}' && http-server -o"
            end tell
        end tell
    end tell
END`
else
    # Could not figure out what the user wants. Dump to console and notify user.
    puts "Could not figure out what to do with data: #{$items.inspect}"
    $dz.fail("Not a file or directory path")
  end
  $dz.finish("Server started")

  $dz.url(false)
end

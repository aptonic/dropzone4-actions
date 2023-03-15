# Dropzone Action Info
# Name: Open Warp at Path
# Description: Drop a file or folder on this action to open a new Warp tab & cd into it. You can also drop a textual path.
# Handles: Files, Text
# Creator: Sachin Shekhar
# URL: https://sachinshekhar.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
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
    
  # Launch Warp tab in desired directory
  if dir
    system("open", "-a", "Warp", dir)
  else
    # Could not figure out what the user wants. Dump to console and notify user.
    puts "Could not figure out what to do with data: #{$items.inspect}"
    $dz.fail("Not a file or directory path")
  end
end

def clicked
  system("open", "-a", "Warp")
end

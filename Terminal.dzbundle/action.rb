# Dropzone Action Info
# Name: Terminal
# Description: Opens a Terminal in the path that is dropped. If a file is given the containing directory will be used. If multiple files are given only the first one is considered
# Handles: Files, Text
# Creator: Dennis Kuypers
# URL: http://dk.kymedia.de
# Events: Clicked, Dragged
# KeyModifiers:
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# MinDropzoneVersion: 3.0

def dragged
    
    # place to store the desired directory
    dir = false
    
    # parse the input
    case ENV['dragged_type']
        when 'files'
        # Get first file and launch in this directory
        dir = File.dirname($items[0])
        when 'text'
        # Verify that this is a directory path
        dir = $items[0] if File.directory?($items[0])
    end
    
    # Launch Terminal in desired directory
    if dir
        system("osascript -e 'tell application \"Terminal\"\n\tactivate\n\tdo script \"cd #{dir};clear\"\nend tell'")
        else
        # Could not figure out what the user wants. Dump to console and notify user.
        puts "Could not figure out what to do with data:"
        puts $items.inspect
        $dz.fail("This is not a file or directory path.")
    end
    
    # nothing to do here...
    $dz.url(false)
end

def clicked
    # FIXME there is probably a way to launch a new window without the "do script" part?
    puts system("osascript -e 'tell application \"Terminal\"\n\tactivate\n\tdo script \"\"\nend tell'")
    # nothing to do here...
    $dz.url(false)
end

# Dropzone Action Info
# Name: Google Maps
# Description: Localise an address with Google Maps, drag an address to the dropzone or click on the action after pasting an address.
# Handles: Text
# Creator: jota3
# URL: https://github.com/jota3
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 168438749

def dragged
    puts $items.inspect
    case ENV['dragged_type']
        when 'text'
        localise_address($items[0])
    end
    $dz.url(false)
end
    
def clicked
    address = $dz.read_clipboard
    localise_address(address)
    $dz.url(false)
end

def localise_address(address)
    gmaps_url = "https://maps.google.com/?q="
    system("open", gmaps_url + address)
end


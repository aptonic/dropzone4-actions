# Dropzone Action Info
# Name: Search Mac App Store
# Description: Searches the Mac App Store for apps with names containing the dragged text or the text on the clipboard when clicked.
# Handles: Text
# Creator: Aptonic Software
# URL: https://aptonic.com
# Events: Clicked, Dragged
# SkipConfig: Yes
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  search($items[0])
end
 
def clicked
  search($dz.read_clipboard)
end

def search(term)
  $dz.begin("Searching Mac App Store...")
  $dz.determinate(false)
  
  url = "itms-apps://search.itunes.apple.com/WebObjects/MZSearch.woa/wa/search?media=software&term=#{term}"
  system("open \"#{url}\"")
  
  $dz.finish("Search Complete")
  $dz.url(false)
end

# Dropzone Action Info
# Name: Open URL in Incognito Mode
# Description: Drop a URL on this action to open it in a new Chrome incognito window. Dropping texts that are not URL causes a Bing search in the incognito mode.
# Handles: Text
# Creator: Sachin Shekhar
# URL: https://sachinshekhar.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0

require 'uri'

def dragged
  url = false
  
  if !!($items[0] =~ /\A#{URI::regexp(['http', 'https'])}\z/)
    url = $items[0]
  else
    url = 'https://www.bing.com/search?q=' + $items[0]
  end
  system("open", "-na", "Google Chrome", "--args", "--incognito", url)
end

def clicked
  system("open", "-na", "Google Chrome", "--args", "--incognito")
end

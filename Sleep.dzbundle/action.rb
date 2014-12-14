# Dropzone Action Info
# Name: Sleep
# Description: Puts your Mac to sleep.
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.0
# RunsSandboxed: No
# UniqueID: 1027
# MinDropzoneVersion: 3.0

def clicked
  $dz.finish("Sleeping...")
  $dz.url(false)
  `osascript -e 'tell application "System Events" to sleep' >& /dev/null`
end

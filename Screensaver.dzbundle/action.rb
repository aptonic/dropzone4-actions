# Dropzone Action Info
# Name: Screensaver
# Description: Starts the screensaver.
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.3
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1006
 
def clicked
  $dz.finish("testing")
  $dz.url(false)
  `osascript -e 'tell application "System Events" to start current screen saver' >& /dev/null`
end

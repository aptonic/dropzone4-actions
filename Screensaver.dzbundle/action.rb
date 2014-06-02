# Dropzone Action Info
# Name: Screensaver
# Description: Starts the screensaver. This is a test update
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.1
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1006
 
def clicked
  $dz.finis("test")
  $dz.url(false)
  `osascript -e 'tell application "System Events" to start current screen saver' >& /dev/null`
end

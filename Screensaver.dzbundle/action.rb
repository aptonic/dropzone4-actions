# Dropzone Action Info
# Name: Screensaver
# Description: Starts the screensaver.
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.1
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1006
 
def clicked
  `osascript -e 'tell application "ScreenSaverEngine" to activate' >& /dev/null`
end

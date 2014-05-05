# Dropzone Action Info
# Name: Screensaver
# Description: Starts the screensaver.
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.0
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
 
def clicked
  `osascript -e 'tell application "System Events" to start current screen saver' >& /dev/null`
end

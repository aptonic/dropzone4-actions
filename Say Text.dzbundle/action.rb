# Dropzone Action Info
# Name: Say Text
# Description: Text dragged onto this action will be read aloud to you.\nClick the action to read text on the clipboard.
# Events: Dragged, Clicked
# Handles: Text
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.2
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1023
 
def dragged
  system "say \"#{$items[0]}\" &"
end

def clicked
	text = readClipboard()
  system "say \"#{text}\" &"
end

def readClipboard
	IO.popen('pbpaste') {|clipboard| clipboard.read}
end
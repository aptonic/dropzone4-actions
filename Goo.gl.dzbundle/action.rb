# Dropzone Action Info
# Name: Goo.gl
# Description: Dropped URLs will be converted to short Goo.gl URLs and short Goo.gl URLs will be expanded. When clicked, the action will attempt to do the same with any URLs present in clipboard.
# Handles: Text
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# Events: Clicked, Dragged
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/urlshortener
# SkipValidation: Yes
# RunsSandboxed: No
# Version: 1.2
# MinDropzoneVersion: 3.2.1
# UniqueID: 1024

require 'googl'

def dragged
  googl = Googl.new

  googl.configure_client
	googl.process($items[0])
end

def clicked
  googl = Googl.new

  googl.configure_client
	data = googl.read_clipboard
	googl.process(data)
end

# Dropzone Action Info
# Name: Goo.gl
# Description: A dropped URL will be converted to a shortened Goo.gl URL.\nYou can also drop shortened URLs to get the expanded URL.\n\nWhen clicked, the action will attempt to shorten or expand a URL on the clipboard.\n\nAuthorization is optional, use it if you want to track the shortened URLs at http://goo.gl using your Google account.
# Handles: Text
# Creator: Dominique Da Silva
# URL: https://inspira.io
# Events: Clicked, Dragged
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/urlshortener
# SkipValidation: Yes
# RunsSandboxed: Yes
# Version: 1.9
# MinDropzoneVersion: 3.2.3
# UniqueID: 1024

require 'googl'

def dragged
  $dz.determinate(false)
  $dz.begin('Getting Goo.gl URL')
  googl = Googl.new

  googl.configure_client
	googl.process($items[0])
end

def clicked
  $dz.determinate(false)
  $dz.begin('Getting Goo.gl URL')
  googl = Googl.new

  googl.configure_client
	data = googl.read_clipboard
	googl.process(data)
end

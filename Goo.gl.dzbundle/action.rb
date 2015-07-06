# Dropzone Action Info
# Name: Goo.gl
# Description: Dropped URLs will be converted to short Goo.gl URLs and short Goo.gl URLs will be expanded. When clicked, the action will attempt to do the same with any URLs present in clipboard.\n\nAuthorization is optional, use it only if you want to track the shortened URLs using your Google account.
# Handles: Text
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# Events: Clicked, Dragged
# OptionsNIB: GoogleAuth
# AuthScope: https://www.googleapis.com/auth/urlshortener
# SkipValidation: Yes
# RunsSandboxed: No
# Version: 1.5
# MinDropzoneVersion: 3.2.1
# UniqueID: 1024
# RubyPath: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/bin/ruby

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

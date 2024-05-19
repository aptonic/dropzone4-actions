# Dropzone Action Info
# Name: Decode Base64
# Description: Decodes the text or the content of the clipboard using Base64 and puts the result in the clipboard. Alt-Drag text to encode.
# Creator: Melvin Gundlach
# URL: http://www.melvin-gundlach.de
# Events: Clicked, Dragged
# Handles: Text
# KeyModifiers: Option
# SkipConfig: Yes
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 23452

require "base64"

def dragged
	$dz.text($items[0])
	clicked
end

def clicked
	modifier = ENV['KEY_MODIFIERS']
	if modifier
		$dz.text(Base64.encode64($dz.read_clipboard))
	else
		$dz.text(Base64.decode64($dz.read_clipboard))
	end
end

# Dropzone Action Info
# Name: Mail A Link
# Description: Drag and drop a link onto this action and a new email will be created in Mail.app with the link.
# Handles: Text
# Creator: Randy Green
# URL: http://humblebeeapps.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# MinDropzoneVersion: 3.0
# UniqueID: 1029

$SUBJECT = "Web Site Link"

def dragged
  $dz.begin("Creating Mail Message with Link...")
        
  `osascript -so <<END
  set theSubject to "#{$SUBJECT}"
  set theBody to "#{$items[0]}"
  set theAddress to "#{$toAddress}"
  tell application "Mail"
  set newMessage to make new outgoing message with properties {subject:theSubject, content:theBody}
  tell newMessage
  set visible to true
  make new to recipient at end of to recipients with properties {address:theAddress}
end tell
activate
end tell
END`

  $dz.finish("Message Created")
  $dz.url(false)
end

def clicked
  system("open /Applications/Mail.app >& /dev/null")
  $dz.url(false)
end

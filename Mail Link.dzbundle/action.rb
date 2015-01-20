# Dropzone Action Info
# Name: Mail A Link
# Description: Drag and drop a link to the "Mail A Link" action and a new email will open.  Fill in a recipient and send off your email.
# Handles: Text
# Creator: Randy Green
# URL: http://humblebeeapps.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID 120112011201

$SUBJECT = "Web Site Link"
$BODY = "Here is your link...\n\n"

def dragged
    
    $dz.begin("Starting Mail A Link...")
        
        case ENV['dragged_type']
            when 'files'
            when 'text'
            `osascript <<-END
            set theSubject to "#{$SUBJECT}"
            set theBody to "#{$BODY} #{$items[0]}"
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
end

$dz.finish("Message Created")

$dz.url(false)
end

def clicked
    # This method gets called when a user clicks on your action
    system("open /Applications/Mail.app >& /dev/null")
    $dz.url(false)
end

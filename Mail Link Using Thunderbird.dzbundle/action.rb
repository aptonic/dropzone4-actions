# Dropzone Action Info
# Name: Mail Link Using Thunderbird
# Description: Drag and drop a link onto this action and a new email will be created in Thunderbird with the link.\n\nNote this action expects Thunderbird to be located at /Applications/Thunderbird.app
# Handles: Text
# Creator: Aptonic Software
# URL: https://aptonic.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0

$SUBJECT = "Website Link"

def dragged
  $dz.begin("Creating Thunderbird Message with Link...")
        
  `osascript -so <<END
  my send_mail("#{$SUBJECT}", "#{$items[0]}")
  
  delay 0.2
  
  tell application "System Events"
  	tell application process "Thunderbird"
  		set frontmost to true
  	end tell
  end tell
  
  on send_mail(email_subject, email_message)
  	try
  		set thunderbird_bin to "/Applications/Thunderbird.app/Contents/MacOS/thunderbird-bin -compose "
  		set email_message to "body=" & email_message
      set email_subject to "subject=" & email_subject
  		set arguments to email_subject & "," & email_message
  		do shell script thunderbird_bin & quoted form of arguments & " > /dev/null 2>&1 &"
  	on error error_message number error_number
  		log error_message & " " & error_number
  	end try
	
  end send_mail
END`

  $dz.finish("Message Created")
  $dz.url(false)
end

def clicked
  system("open /Applications/Thunderbird.app >& /dev/null")
  $dz.url(false)
end

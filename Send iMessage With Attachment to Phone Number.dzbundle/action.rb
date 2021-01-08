# Dropzone Action Info
# Name: Send iMessage With Attachment to Phone Number
# Description: Send an iMessage with a file attachment to a preset phone number.\n\nClick the action in the grid to set the phone number.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.5
# MinDropzoneVersion: 3.0
# UniqueID: 1021

def dragged
  $dz.begin("Sending iMessage...")
  
	# Try to get remote container name from saved values
	unless ENV['phone_number']
		phone_number = read_phone_number
	else
		phone_number = ENV['phone_number'].dup
	end

  # If not available, then read it and save it
  if phone_number.to_s.strip.length == 0
    phone_number = read_phone_number
  end
  
  # Send each dropped file
  $items.each do |path|
    phone_number.gsub!("\"", "\\\"")
    path.gsub!("\"", "\\\"")
    result=`osascript -so <<END
set theAttachment1 to POSIX file "#{path}"
tell application "Messages"
  set targetService to 1st service whose service type = iMessage
  set targetBuddy to buddy "#{phone_number}" of targetService
  send theAttachment1 to targetBuddy
  try
    close window "File Transfers"
  end try
end tell
tell application "Finder"
  try
    set visible of process "Messages" to false
  end try
end tell
END`
  puts result

  $dz.error("Failed to send iMessage", "Failed to send to contact. Try opening iMessage and sending a message to this number manually first, then try again with Dropzone.") if result =~ /Can’t get buddy id/
  $dz.error("Failed to send iMessage", "Failed to send iMessage to the entered phone number.\n\n#{result}") if result =~ /error/
  end
  
  $dz.finish("iMessage Sent")
  $dz.url(false)
end
 
def clicked
  read_phone_number
  $dz.finish('New phone number saved')
  $dz.url(false)
end

def read_phone_number
  config = "
  *.title = Phone Number
  p.type = textfield
  p.width = 500
  p.label = Enter the phone number to send to (this will be saved so you only have to enter it once):
  cb.type = cancelbutton
  "
  result = $dz.pashua(config)
  
  if result['cb'] == '1'
    $dz.fail('Cancelled')
  end

  phone_number = result['p']

  # Fail if no phone number is entered
  if phone_number.to_s.strip.length == 0
    $dz.fail('Phone number cannot be empty.')
  else
    $dz.save_value('phone_number', phone_number)
  end

  phone_number
end

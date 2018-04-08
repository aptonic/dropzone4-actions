# Dropzone Action Info
# Name: Screenshot
# Description: Take a screenshot, add it to ~/Screenshots and add to Drop Bar
# Creator: Gareth Evans
# URL: http://yoursite.com
# Events: Clicked
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 1037

def clicked
  # Create the Screenshots directory if not already present
  system("mkdir ~/Screenshots")
  
  # Make a filename with the current time
  formatted_time = Time.now.strftime("%F at %I.%M.%S %p")
  filename = "Screen Shot " + formatted_time + ".png"
  file_path = File.expand_path('~') + "/Screenshots/" + filename
  
  # Capture screenshot
  system("screencapture -i \"" + file_path + "\"")
  
  # Add to Drop Bar
  $dz.add_dropbar([file_path])
  
  # Notification
  $dz.finish("Screenshot added")
  $dz.url(false)
end

# Dropzone Action Info
# Name: Finder Path
# Description: Click on this action to copy the path of the currently selected item in the Finder to the clipboard.\n\nYou can also drag files onto it and it will put the paths of the dragged files on the clipboard.
# Creator: Aptonic Software
# URL: http://aptonic.com
# Events: Clicked, Dragged
# Handles: Files
# SkipConfig: Yes
# RunsSandboxed: No
# Version: 1.3
# MinDropzoneVersion: 3.0
# UniqueID: 1003

require 'shellwords'

def dragged
  file_path_list = ""
  $items.each {|item| file_path_list += Shellwords.shellescape(item.strip) + "\n"}
  
  s = ($items.length > 1 ? "s" : "")
  $dz.finish("Path" + s + " copied")
  $dz.text(file_path_list.strip)
end
  
def clicked

path=`osascript <<END
tell application "Finder"
	try
		set theSelection to (target of window 1 as alias)
		set theSelection to theSelection as string
		set finder_path to POSIX path of (the selection as alias)
	on error
		set finder_path to null
	end try
end tell
if finder_path is not null then return finder_path
END`

  if (path == nil or path == "")
    $dz.finish("Nothing selected")
    $dz.url(false)
  else 
    $dz.finish("Path copied")
    $dz.text(path.strip)
  end
  
end

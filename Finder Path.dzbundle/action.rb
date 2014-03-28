# Dropzone Action Info
# Name: Finder Path
# Description: Copies the path of the currently selected item in the Finder to the clipboard.
# Handles: Files
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.0
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0

def clicked

path=`osascript <<END
tell application "Finder"
	try
		set theSelection to (target of window 1 as alias)
		set theSelection to theSelection as string
		set finder_path to POSIX path of theSelection
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
    $dz.text(path)
  end
  
end

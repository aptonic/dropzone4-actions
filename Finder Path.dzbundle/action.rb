# Dropzone Action Info
# Name: Finder Path
# Description: Copies the path of the currently selected item in the Finder to the clipboard.
# Events: Clicked
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.1
# SkipConfig: Yes
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1003

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
    $dz.finish("Testing")
    $dz.url(false)
  else 
    $dz.finish("Path copied")
    $dz.text(path.strip)
  end
  
end

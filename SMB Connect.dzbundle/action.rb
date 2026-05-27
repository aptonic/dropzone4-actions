# Dropzone Action Info
# Name: SMB Connect
# Description: Mounts an SMB/Windows share and opens it in Finder. Click to mount and open. Drag files to copy them to the share root.
# Handles: Files
# Creator: edenraf
# URL: https://github.com/edenraf
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.3
# MinDropzoneVersion: 4.0
# OptionsNIB: ExtendedLogin

require 'smb_connect'

def clicked
  $dz.determinate(false)
  mounter = SMBConnect.new
  mounter.connect
end

def dragged
  $dz.determinate(true)
  mounter = SMBConnect.new
  mounter.copy_files($items)
end

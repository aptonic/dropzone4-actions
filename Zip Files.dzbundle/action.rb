# Dropzone Action Info
# Name: Zip Files
# Description: Zips up the dropped files or folders and places the zip file in the chosen folder.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ChooseFolder
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# MinDropzoneVersion: 3.2.1
# UniqueID: 1025

def dragged
  $dz.determinate(false)
  filename = $dz.inputbox("New ZIP File", "Enter name for new zip file (minus extension):")
  zipfile = ZipFiles.zip($items, filename + ".zip")
  zipfile = zipfile[1, zipfile.length - 2]
  system("zip -d \"#{zipfile}\" '__MACOSX*' '*.DS_Store' >& /dev/null")
  Rsync.do_copy([zipfile], ENV['path'], true)
  $dz.finish("ZIP created")
  $dz.url(false)
end

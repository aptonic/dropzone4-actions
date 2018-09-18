# Dropzone Action Info
# Name: Zip by Parent Name
# Description: Zip up multiple files and naming by the parent directory's name.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ChooseFolder
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.2
# MinDropzoneVersion: 3.2.1

def dragged
  $dz.determinate(false)
  filename = File.basename(File.dirname($items[0]))
  parentdir = File.dirname($items[0])
  zipfile = ZipFiles.zip($items, filename + ".zip")
  zipfile = zipfile[1, zipfile.length - 2]
  system("zip -d \"#{zipfile}\" '__MACOSX*' '*.DS_Store' >& /dev/null")
  Rsync.do_copy([zipfile], parentdir, true)
  $dz.finish("ZIP created")
  $dz.url(false)
end

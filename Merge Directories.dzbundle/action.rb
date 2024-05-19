# Dropzone Action Info
# Name: Merge Directories
# Description: Takes directories as the input. Each directory should have the same number of files. The files are combined into a zip: one from each directory in order.
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.2
# MinDropzoneVersion: 3.2.1

def dragged
	#
	# Begin the Action.
	#
	$dz.determinate(true)
	mainDir = File.dirname($items[0])

	#
	# Create the Zip directory.
	#
  zipDir = File.join(mainDir,"Zips")
	Dir.mkdir(zipDir)

  #
  # Get a list of each directories files.
  #
  dirList = Array.new
  $items.each_index { |index|
    dirList[index] = Dir.entries($items[index])
    dirList[index].delete(".")
    dirList[index].delete("..")
    dirList[index].delete(".DS_Store")
  }
  numFiles = dirList[0].length

	#
	# Create the Zip files in the zipDir.
	#
  for index in (0..(numFiles-1)) do
    files = Array.new()
    $items.each_index { |inner|
      files[inner] = File.join($items[inner],dirList[inner][index])
    }
    filename = File.basename(files[0],".*") + ".zip"
  	zipfile = ZipFiles.zip(files, filename)
    zipfile = zipfile[1, zipfile.length - 2]

    #
    # Remove the OS X files from the zip file.
    #
    system("zip -d \"#{zipfile}\" '__MACOSX*' '*.DS_Store' >& /dev/null")

    #
    # Move the zip to the directory of the files.
    #
    Rsync.do_copy([zipfile], "#{zipDir}/#{filename}", true)

    #
    # Set the percentage done.
    #
    $dz.percent((index/numFiles)*100)
  end

	#
	# Finalize.
	#
	$dz.finish("ZIPs created")
	$dz.url(false)
end

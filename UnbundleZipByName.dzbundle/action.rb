# Dropzone Action Info
# Name: Unbundle Zip by Name
# Description: This action will unzip a zip file into the curret directory and rename the files to the name of the zip file.
# Handles: Files
# Events: Dragged
# Creator: Richard Guay <raguay@customct.com>
# RunsSandboxed: Yes
# Version: 1.0
# URL: http://customct.com
# MinDropzoneVersion: 3.0
# UniqueID: 1008

require 'fileutils'

def dragged
	#
	# Turn on determinate mode.
	#
	$dz.determinate(true)

	#
	# Process each zip file.
	#
	total = $items.count

	#
	# Set default result message.
	#
	result = "Not a Zip file!"

	#
	# Tell dropzone we are starting...
	#
	$dz.begin("Start compressing #{total} images...")

	#
	# Index over all of the given images.
	#
	for index in 0 ... total
		#
		# Determine if it is a zip file.
		#
		ext = File.extname($items[index])
		if ext == ".zip"
			#
			# Get the file name
			#
			zipname = File.basename($items[index],".zip")
			zippath = File.dirname($items[index])

			#
			# Extract the files.
			#
			`/usr/bin/unzip "#{zippath}/#{zipname}.zip" -d "#{zippath}/#{zipname}/"`

			#
			# change each file to the new basename based on zip file's name.
			#
			Dir.foreach("#{zippath}/#{zipname}") {|filename|
				if (filename != ".") && (filename != "..")
					ext = File.extname(filename)
					File.rename("#{zippath}/#{zipname}/#{filename}", "#{zippath}/#{zipname}/#{zipname}#{ext}")
				end
			}

			#
			# Tell Dropzone what percentage is done.
			#
			$dz.percent((((index + 1)*100)/total).to_i)

			#
			# Set the results string to finished.
			#
			result = "Finished Extraction."
		end
	end

	#
	# Tell the user that it is done.
	#
	$dz.finish(result)

	#
	# Finish out the dropzone protocal. If you want a url in the clipboard, pass it
	# here. If you just want to copy text to the clipboard, use $dz.text() instead.
	# Either $dz.url() or $dz.text() has to be the last thing in the dragged method.
	#
	$dz.url(false)
end

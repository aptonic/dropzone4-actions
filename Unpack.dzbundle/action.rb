# Dropzone Action Info
# Name: Unpack
# Description: This action unpack zip files in to a specified directory.
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.2
# OptionsNIB: ChooseFolder
# UniqueID: 234985238238452835

def dragged
	#
	# Turn on determinate mode.
	#
	$dz.determinate(true)

	#
	# Get the data values.
	#
	if ( (ENV['path'] != nil) && (File.directory?(ENV['path'])) )
		#
		# get the defaults.
		#
		dir = ENV['path']

		#
		# Process each image file.
		#
		total = $items.count

		#
		# Tell dropzone we are starting...
		#
		$dz.begin("Unpacking #{total} files...")

		#
		# Index over all of the given images.
		#
		for index in 0 ... total
			#
			# Convert the image file.
			#
			`/usr/bin/unzip  -n "#{$items[index]}" -d "#{dir}" `

			#
			# Delete the original file.
			#
			File.delete($items[index])

			#
			# Tell Dropzone what percentage is done.
			#
			$dz.percent((((index + 1)*100)/total).to_i)
		end
	else
		#
		# The user did not configure the action. Tell them.
		#
		$dz.error("Unpack Action", "You did not give a target directory!")
	end

	#
	# Tell the user that it is done.
	#
	$dz.finish("Finished Unpacking.")

	#
	# Finish out the dropzone protocal. If you want a url in the clipboard, pass it
	# here. If you just want to copy text to the clipboard, use $dz.text() instead.
	# Either $dz.url() or $dz.text() has to be the last thing in the dragged method.
	#
	$dz.url(false)
end

def clicked
	#
	# The clicked handler should get the destination directory to use and
	# save it.
	#

	#
	# Request the width of the graphic.
	#
	dir =$dz.cocoa_dialog("fileselect --select-directories ‑‑select‑only-directories  --title 'Unpack to Directory' ").split("\n")

	#
	# See if the user canceled out. Do not continue if they cancel.
	#
	if ((dir[0] != nil)&&(File.directory?(dir[0])))
		#
		# Save the directory location.
		#
		$dz.save_value("path", dir[0])

	else
		#
		# The user did not configure the action. Tell them.
		#
		$dz.error("Unpack Action", "You canceled out! You did not give a target directory!")
	end

	#
	# Tell the user that it is done.
	#
	$dz.finish("Unpack Directory: #{dir[0]}")

	#
	# Finish out the dropzone protocal. If you want a url in the clipboard, pass it
	# here. If you just want to copy text to the clipboard, use $dz.text() instead.
	# Either $dz.url() or $dz.text() has to be the last thing in the clicked method.
	#
	$dz.url(false)
end

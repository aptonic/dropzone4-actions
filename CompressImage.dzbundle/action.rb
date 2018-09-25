# Dropzone Action Info
# Name: Compress Image
# Description: This destination is for compressing the images given.\n\nYou must have the imagemagick library installed. It is best to install it using HomeBrew (http://brew.sh/).
# Handles: Files
# Events: Clicked, Dragged
# Creator: Richard Guay <raguay@customct.com>
# RunsSandboxed: Yes
# Version: 1.2
# URL: http://customct.com
# MinDropzoneVersion: 3.6
# UniqueID: 1008

require 'fileutils'

def dragged
	#
	# Turn on determinate mode.
	#
	$dz.determinate(true)

	#
	# Set the default return string to an error.
	#
	result = "You have to set the defaults first!"

	#
	# Get the data values.
	#
	#
	# get the defaults.
	#
	$size = ENV['image_width']
	$ext = ENV['image_ext']

	#
	# Process each image file.
	#
	total = $items.count

	#
	# Tell dropzone we are starting...
	#
	$dz.begin("Start compressing #{total} images...")

	#
	# Create the temporary directory for the originals.
	#
	tmpDir = File.dirname($items[0]) + "/tmp/"
	if ! File.directory?(tmpDir)
		#
		# Directory does not exist! Create it!
		#
		FileUtils.mkdir_p(tmpDir)
	end


	#
	# Index over all of the given images.
	#
	for index in 0 ... total
		#
		# Copy the original to the tmp directory. Rsync would be the preferred
		# method, but it messes up the percentage graph on the user interface.
		#
		# Rsync.do_copy($items[index], tmpDir, false)
		#
		FileUtils.copy_file($items[index], "#{tmpDir}#{File.basename($items[index])}")

		#
		# Create the new file name with the extension supplied by the user.
		#
		$newFilePath = "#{$items[index].chomp(File.extname($items[index]))}#{$ext}"

		#
		# Convert the image file.
		#
		`/usr/local/bin/convert  -background white -quality 90% -alpha background -alpha off +dither -colors 512 -flatten -transparent none -resize #{$size} \"#{$items[index]}\" \"#{$newFilePath}\";`

		#
		# If the conversion does not destroy the original, then remove the original.
		#
		if File.extname($items[index]) != $ext
			File.delete($items[index])
		end

		#
		# Tell Dropzone what percentage is done.
		#
		$dz.percent((((index + 1)*100)/total).to_i)

		#
		# Set the results string to finished.
		#
		result = "Finished Compressing."
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

def clicked
	#
	# The clicked handler should get the size and extension to use and
	# save it in the configuration file. We will save data in the
	# ~/Library/Application Support/Dropzone/Destination Data/CompressFiles.txt
	#
	$size = ENV['image_width']
	$ext = ENV['image_ext']

	#
	# Ask for the graphic file type to end up with.
	#
	config = "
		*.title = Compress Files
		gf.type = popup
		gf.option = .jpg
		gf.option = .png
		gf.option = .gif
		gf.default = #{$ext}
  		gf.label = What graphics format?
  		gw.type = textfield
  		gw.label = What size in px?
  		gw.default = #{$size}
		"
	result = $dz.pashua(config)
	ext = result["gf"]
	width = result["gw"]

	#
	# Write the data file. Do not append, but delete and write fresh!
	#
	$dz.save_value("image_width", width)
	$dz.save_value("image_ext", ext)

	#
	# Tell the user by setting the return string to what the user gave.
	#
	result = "Size: #{width} px, Ext: #{ext}"

	#
	# Tell the user that it is done.
	#
	$dz.finish(result)

	#
	# Finish out the dropzone protocal. If you want a url in the clipboard, pass it
	# here. If you just want to copy text to the clipboard, use $dz.text() instead.
	# Either $dz.url() or $dz.text() has to be the last thing in the clicked method.
	#
	$dz.url(false)
end

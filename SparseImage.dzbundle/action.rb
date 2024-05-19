# Dropzone Action Info
# Name: Sparse Image
# Description: Creates a Sparse Image with dropped files and places it on the Desktop.\nHolding the Option key while dragging creates an AES-256 bits encrypted Sparse image.
# Handles: Files
# Creator: Dominique Da Silva
# URL: https://apps.inspira.io
# Events: Clicked, Dragged
# KeyModifiers: Option
# SkipConfig: No
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# Version: 1.1
# UniqueID: 7003

$tmpDir = $dz.temp_folder + '/dztmp-' + Time.now.usec.to_s

def dragged
	fileName = $dz.inputbox("New Sparse Image File", "Enter name for new Sparse file:", "Sparse Name")

	# output name (remove the filename and any other chars that could be potentially dangerous)
	fileName = File.basename(fileName, '.*').gsub(/[^a-zA-Z0-9\.\s-]/, '')

	# set the output file and volume name
	imageName = fileName + '.sparseimage'
	volumeName = fileName

	tmpSrcDir = "#{$tmpDir}/src";

	# set the output files
	tmpSparseImage = "#{$tmpDir}/#{imageName}"
	destination = ENV['HOME'] + '/Desktop'

	# make sure the destination directory is there and writable
	if File.exists?(destination) == false && File.directory?(destination) == false
		$dz.error("Directory Error.", "Unable to find the destination directory")
		return
	end

	# create the tmp directories and copy the files across
	begin
		# check to see if the file is a directory (and not an app), and if so then only copy the contents of that folder and not the parent dir like DropDMG
		files = []
		if $items.length == 1 and File.directory?($items[0]) and File.extname($items[0]) != '.app'
			Dir.entries($items[0]).each do |file|
				if file != '.' and file != '..' and file != '.DS_Store'
					# get the full path to the directory
					files.push($items[0] + '/'  + file)
				end
			end
		end

		# create the tmp dir where we will do all the work
		system("/bin/mkdir -p \"#{tmpSrcDir}\"")

		# if we have passed in a directory and there are files in it, then copy those otherwise just copy the dragged src
		$dz.determinate(true)
		if files.length > 0
			$dz.begin("Copying directory contents...")
			Rsync.do_copy(files, tmpSrcDir, false, true)
		else
			$dz.begin("Copying files...")
			Rsync.do_copy($items, tmpSrcDir, false, true)
		end

	rescue => e
		cleanup
		$dz.error("Error Copying files...", e.message)
		return
	end

	# create the image file, copy to the desktop and do some cleaning up
	begin

		puts "Temporary source directory: #{tmpSrcDir}"

		$dz.begin("Calculating final Image Size...")

		folder_size = Dir.glob(File.join(tmpSrcDir, '**', '*'))
					.map{ |f| File.size(f) }
					.inject(:+)
		sparse_size = [1, (folder_size / 1000000000.0).ceil].max.to_s + "g"

		puts "Calculated folder size #{folder_size/1000000.0}Mb, creating an image of #{sparse_size}."

		# create an encrypted sparse image if a modifier key is held down
		if ENV["KEY_MODIFIERS"] != "Option"
			$dz.determinate(false)
			$dz.begin("Creating Sparse Image...")
			system("hdiutil create -srcfolder \"#{tmpSrcDir}\" -format UDSP -size #{sparse_size} -volname \"#{volumeName}\" \"#{tmpSparseImage}\" >& /dev/null")
		else
			# get the password
			pconfig = "
				*.title = Secure Sparse Image
				p.type = textfield
				p.label = Enter a new password to secure \"#{imageName}\"
				p.mandatory = true
				i.type = text
				i.default = If you forget this password you will not be able to access the files stored on this AES-256 encrypted image.
				bc.type = cancelbutton
				bc.default = Cancel
			"
			$dz.begin("Waiting for the Sparse Image password...")
			output = $dz.pashua(pconfig)
			password = output['p']

			# stop on cancel
			if output['bc'] == '1'
				cleanup
				$dz.fail("Sparse Image creation cancelled.")
				$dz.url(false)
				return
			end

			$dz.determinate(false)
			$dz.begin("Creating Encrypted Sparse Image...")

			system("echo \"#{password}\\0\" | hdiutil create -srcfolder \"#{tmpSrcDir}\" -encryption \"AES-256\" -stdinpass -size #{sparse_size} -format UDSP -volname \"#{volumeName}\" \"#{tmpSparseImage}\" -ov >& /dev/null")
		end

		# move the Image to the desktop
		$dz.begin("Moving Sparse to destination...")
		$dz.determinate(true)
		Rsync.do_copy([tmpSparseImage], destination, false, true)

		# do come cleanup
		cleanup

		$dz.finish('Sparse Image Created');
		$dz.url(false)
	rescue => e
		cleanup
		$dz.error("Error Creating Sparse Image File", e.message)
		return
	end
end

def clicked
	# open the Disk Utility app in the Utilities folder
	`osascript -e 'tell application "Disk Utility" to activate'`
end

def cleanup
	# remove the tmp directory
	if File.exists?($tmpDir)
		system("/bin/rm -rf \"#{$tmpDir}\" >& /dev/null")
	end
end

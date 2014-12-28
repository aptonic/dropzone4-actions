# Dropzone Action Info
# Name: Create DMG File
# Description: Creates a DMG file with dropped files and places it on the Desktop.\nHolding the Option key while dragging creates an encrypted DMG.
# Handles: Files
# Events: Clicked, Dragged
# KeyModifiers: Option
# Creator: Megan Cooke
# URL: http://www.insanekitty.co.uk
# Version: 1.0
# RunsSandboxed: No
# UniqueID: 1028
# MinDropzoneVersion: 3.0

$tmpDir = $dz.temp_folder + '/dztmp-' + Time.now.usec.to_s

def dragged
  fileName = $dz.inputbox("New DMG File", "Enter name for new DMG file:", "DMG Name")

	# output name (remove the filename and any other chars that could be potentially dangerous)
	fileName = File.basename(fileName, '.*').gsub(/[^a-zA-Z0-9\.\s-]/, '')

	# set the output dmg and volume name
	dmgName = fileName + '.dmg'
	volumeName = fileName
	
	tmpSrcDir = "#{$tmpDir}/src";
	
	# set the output files
	tmpDmg = "#{$tmpDir}/#{dmgName}"
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

	# create the dmg file, copy to the desktop and do some cleaning up
	begin
		
		# create an encrypted DMG file if a modifier key is held down
		if ENV["KEY_MODIFIERS"] != "Option"
			$dz.determinate(false)
			$dz.begin("Creating DMG file...")
			system("hdiutil create \"#{tmpDmg}\" -volname \"#{volumeName}\" -srcfolder \"#{tmpSrcDir}\" -ov >& /dev/null")
		else
			# get the password
			output = $dz.cocoa_dialog('secure-standard-inputbox ‑‑float --title "Enter a new password to secure ' + dmgName + '" --e --informative-text "If you forget this password you will not be able to access the files stored on this image.' + "\n\n" + 'Enter the password:" --button1 "Ok" --button2 "Cancel"')
			button, password = output.split("\n")
			
			# stop on cancel
			if button == "2"
				cleanup
				$dz.finish("Cancelled")
				$dz.url(false)
				return
			end
			
			$dz.determinate(false)
			$dz.begin("Creating Encrypted DMG file...")

			# man hdiutil
			# create the encrypted image (-stdinpass reads a null-terminated passphrase from standard input so need to create a null terminated string)
			system("echo \"#{password}\\0\" | hdiutil create -encryption -stdinpass -volname \"#{volumeName}\" -srcfolder \"#{tmpSrcDir}\" \"#{tmpDmg}\" -ov >& /dev/null")
		end

		# move the dmg to the desktop
		$dz.begin("Moving DMG to destination...")
		$dz.determinate(true)
		Rsync.do_copy([tmpDmg], destination, false, true)

		# do come cleanup
		cleanup

		$dz.finish('DMG Created');
		$dz.url(false)
	rescue => e
		cleanup
		$dz.error("Error Creating DMG File", e.message)
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

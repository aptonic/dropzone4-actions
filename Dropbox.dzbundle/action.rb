# Dropzone Action Info
# Name: Dropbox
# Description: Share files via Dropbox by copying them to your Dropbox Public folder and putting the URL on the clipboard.
# Handles: Files
# Creator: Philipp Fehre
# URL: http://sideshowcoder.com
# Events: Dragged, Clicked
# OptionsNIB: DropboxLogin
# Version: 1.0
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1010

require 'set'
require 'base64'

# Global variables for Dropbox settings
@dropboxPubDir = ""
@dropboxPublicBaseURL = "http://dl.dropbox.com/u/"

def dropbox?
	# Get Dropbox Public directory from the Dropbox database file, if this file is not present
	# Dropbox is most likely not installed
	if File.exist?(conf_path = ENV['HOME'] + '/.dropbox/host.db')
	  @dropboxPubDir = Base64.decode64(File.open(conf_path).read).match(/\/.+$/)[0] + '/Public'
	  return true
  else
    return false
  end
end


def dragged
	$dz.determinate(true)
	# Check if Dropbox is installed and set Public path
	if not dropbox?
		$dz.finish("Dropbox is not installed")
		$dz.url(false)
		return
	end

	# Handle Drag
	if $items.length > 1
		# More than 1 item dragged 
		# Create zip of all items and name it after the first item
		dir_name = /\A(\w*)/.match($items[0].split(File::SEPARATOR).last)
		zipfile = ZipFiles.zip($items, "#{dir_name}.zip")
		path = zipfile
	elsif File.directory?($items[0])
		# 1 Folder was dragged
		# Create a Zip from the folder and name it after the folder
		dir_name = $items[0].split(File::SEPARATOR).last
		zipfile = ZipFiles.zip($items[0], "#{dir_name}.zip")
		path = zipfile
	else
		# Only 1 item dragged 
		# Handle only the file by itself
		path = $items[0]
	end
	
	
	# Need to strip quotes which are passed when using a Zipfile
	# This might be a ruby bug but the regexp should take care of that even if it is fixed
	# some time in the futur
	path.gsub!(/\A(['"])(.*)\1\z/, '\2')

	# Copy file to Dropbox Public dir and place create URL on Clipboard
	$dz.begin("Copying #{File.basename(path)} ...")
	Rsync.do_copy(path, @dropboxPubDir, false)
	$dz.finish("URL is now on clipboard")
	$dz.url("#{@dropboxPublicBaseURL}#{ ENV['user_id']}/#{File.basename(path)}")
end

def clicked
	# Check for Dropbox and set Public Directory path
	if not dropbox?
		$dz.determinate(false)
		$dz.finish("Dropbox is not installed")
		$dz.url(false)
	else
		# Open Finder at Public Directory using Applescript
		`osascript -e 'tell application "Finder"' -e 'activate' -e 'open folder\
		POSIX file "#{@dropboxPubDir}"' -e 'end tell'`
	end
end
    

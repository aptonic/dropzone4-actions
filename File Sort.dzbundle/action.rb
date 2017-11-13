# Dropzone Action Info
# Name: File Sort
# Description: Auto move a file to its corresponding folder if a part of the filename match the folder name.
# Handles: Files
# Creator: Dominique Da Silva
# URL: https://inspira.io
# OptionsNIB: ChooseFolder
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# Version: 1.1
# UniqueID: 7001

require 'FileUtils'

@folderlist = Array.new
@destination = ""
@log = ""
@fail = ""

def checkFilenameMatch(str)
	titlePart = str.downcase
	puts "Search for #{titlePart.downcase}"
	destination = @folderlist.select {|e| e.downcase =~ /#{titlePart}/ }.first
	return destination
end

def dragged

	folder      = ENV['path']
	@folderlist = Dir.glob "#{folder}/*/"

	$items.each do |filepath|
		filename = File.basename(filepath)
		filetitle = File.basename(filepath,".*")
		#*filetitleArr, ext = filetitle.split(/\W/)
		filetitleArr = filetitle.split(/\W/)
		@destination = ""

		puts filetitle.inspect
		puts filetitleArr.inspect

		# First two words in filename
		if filetitleArr.count >= 2
			@destination = checkFilenameMatch("#{filetitleArr[0]} #{filetitleArr[1]}")
		end

		# Last two words in filename
		if filetitleArr.count > 2 && (@destination.nil? || @destination.empty?)
			last2Parts = Array.new
			filetitleArr.reverse.each do |part|
				if part.length > 2 and part !~ /^[0-9]+$/
					last2Parts.push(part)
				end
				if last2Parts.count == 2 then
					break
				end
			end
			@destination = checkFilenameMatch(last2Parts.reverse.join(" "))
		end

		# Search for all parts of filename
		if @destination.nil? || @destination.empty?
			filetitleArr.each do |titlePart|
				if titlePart.length > 2 and titlePart !~ /^[0-9]+$/
					@destination = checkFilenameMatch(titlePart)
					if !@destination.nil? then break; end
				end
			end
		end

		if !@destination.nil?
			puts "Found destination! Move file to #{@destination}"
			$dz.begin("Moving \"#{filename}\" to #{@destination}...")
			FileUtils.mv(filepath, @destination)
			system("open \"#{@destination}\"")
			@log = "[Done] Moved \"#{filename}\" to #{File.basename(@destination)}.\n#{@log}"
		else
			puts "Folder for \"#{filename}\" not found!"
			@fail = "[Fail] Folder for \"#{filename}\" not found!\n#{@fail}"
		end
	end

	if @fail.empty? then
		$dz.finish("Finishing sorting files.")
	else
		$dz.finish("Finishing sorting files with errors.")
	end
	$dz.url(false)
	$dz.alert("File Sort for "+File.basename(folder),"#{@log}--\n#{@fail}")
end

def clicked
  folder = ENV['path']
  system("open \"#{folder}\"")
end

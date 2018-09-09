# Dropzone Action Info
# Name: Convert to MP4
# Description: Converts the dropped videos to the MP4 format using ffmpeg. Alt-Drag to trash source files after conversion. Hold down Shift to convert to HEVC. Hold down Command to only change container without converting. Hold down Control to extract audio (only works with aac).
# Creator: Melvin Gundlach
# URL: http://www.melvin-gundlach.de
# Events: Clicked, Dragged
# Handles: Files
# KeyModifiers: Command, Option, Control, Shift
# RunsSandboxed: Yes
# SkipConfig: Yes
# Version: 1.1
# MinDropzoneVersion: 3.0
# UniqueID: 23451

def dragged
	$dz.begin("Converting files...")
	$dz.determinate(true)
	$dz.percent(0)
	currentFileNumber = 0
	
	$items.each { |itemX|
		basename = File.basename(itemX, ".*")
		puts basename
		filepath = File.dirname(itemX)
		puts filepath
		
		requestString = "/usr/local/bin/ffmpeg -i \"#{itemX}\" \"#{filepath}\"/\"#{basename}\".mp4"
		if ENV['KEY_MODIFIERS'] == "Command" # Codec copy
			requestString = "/usr/local/bin/ffmpeg -i \"#{itemX}\" -codec copy \"#{filepath}\"/\"#{basename}\".mp4"
			filepath += "/" + basename + ".mp4"
		elsif ENV['KEY_MODIFIERS'] == "Shift" # x265
			requestString = "/usr/local/bin/ffmpeg -i \"#{itemX}\" -codec:video libx265 \"#{filepath}\"/\"#{basename}\".mp4"
			filepath += "/" + basename + ".mp4"
		elsif ENV['KEY_MODIFIERS'] == "Control" # Excract m4a audio
			requestString = "/usr/local/bin/ffmpeg -i \"#{itemX}\" -vn -codec copy \"#{filepath}\"/\"#{basename}\".m4a"
			filepath += "/" + basename + ".m4a"
		else
			filepath += "/" + basename + ".mp4"
		end
		ret = system(requestString)
		
		puts filepath
		
		if !ret
			failString = "Have you installed ffmpeg? Is your input valid?"
			if ENV['KEY_MODIFIERS'] == "Command" # Codec copy
				failString += "\nInput video codec not compatible with MP4 container. Possibly source file is MP4 file already."
				elsif ENV['KEY_MODIFIERS'] == "Shift" # x265
				failString += "\nMaybe you don't have the libx265 library for ffmpeg installed. Possibly source file is MP4 file already."
				elsif ENV['KEY_MODIFIERS'] == "Control" # Excract m4a audio
				failString += "\nInput audio codec is not aac."
			end
			
			$dz.error("Error", failString)
			
			$dz.fail(failString)
		else
			$dz.save_value('filepath', filepath)
			if ENV['KEY_MODIFIERS'] == "Option"
				`osascript -e 'tell application "Finder" to move the POSIX file "#{itemX}" to trash' >& /dev/null`
			end
		end
		
		currentFileNumber += 1
		$dz.percent(currentFileNumber * 100 / $items.count)
	}
	
	$dz.finish("Done converting")
	$dz.url(false)
end
 
def clicked
	if ENV['filepath']
		path = ENV['filepath']
		puts path
		`osascript -e 'tell application "Finder" to reveal the POSIX file "#{path}"' >& /dev/null`
		`osascript -e 'tell application "Finder" to activate' >& /dev/null`
	end
end

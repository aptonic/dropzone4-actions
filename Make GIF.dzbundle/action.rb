# Dropzone Action Info
# Name: Make GIF
# Description: This action converts videos to GIFs using ffmpeg
# Handles: Files
# Creator: BlahGeek
# URL: http://blahgeek.com
# Events: Clicked, Dragged
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# OptionsNIB: ChooseFolder

def dragged
	$dz.determinate(false)

	path = ENV['path']
	if !File.directory?(path)
		$dz.error("Please set a output directory")
	end

	basename = File.basename($items[0])
	ret = system("/usr/local/bin/ffmpeg -i \"#{$items[0]}\" -pix_fmt rgb24 -r 5 \"#{path}\"/\"#{basename}\".gif")

	if !ret
		$dz.fail("Have you installed ffmpeg? Or is your input valid?")
	else
		$dz.finish("Done making GIF")
		$dz.url(false)
	end
end

def clicked
	path = ENV['path']
	if !File.directory?(path)
		$dz.error("Please set a output directory")
	end
	`open #{path}`
end

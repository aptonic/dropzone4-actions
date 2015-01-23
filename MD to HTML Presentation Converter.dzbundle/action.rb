# Dropzone Action Info
# Name: MD to HTML Presentation Converter
# Description: Takes a markdown file and converts it to an HTML/CSS presentation in the files directory. It assumes you have kramdown installed locally. To install, go to a commandline and type "sudo gem install kramdown".
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

#
# Function: 	dragged
#
# Description: This function is called with Dropzone has files dropped on this action.
# 					It then processed each given file as a markdown presentation.
#
def dragged
	#
	# Set some variables.
	#
	$presDir = ""
	pressBaseDir = File.expand_path(".")
	presNum = $items.count
	theme = defined?( ENV['theme'] ) ? ENV['theme'] : "Basic"

	#
	# Tell Dropzone we are starting.
	#
	$dz.begin("Converting #{presNum} Presentations...")
	$dz.determinate(true)

	#
	# Get the slide presentation parts loaded.
	#
	presBegin = `cat '#{pressBaseDir}/presbegin.html'`
	presEnd = `cat '#{pressBaseDir}/presend.html'`

	#
	# Index over all of the given presentations.
	#
	for index in 0 ... presNum
		#
		# Get the directory of the presentation.
		#
		$presDir = File.dirname($items[index])

		#
		# Convert the Markdown to HTML.
		#
		presTextHTML = `cat '#{$items[index]}' | kramdown`

		#
		# Convert the horizontal rules to the divs we need.
		#
		$divCount = 1
		while presTextHTML.sub!(/\<hr \/\>/, "</div></div><div id='section#{$divCount}' class='section'><div class='slide'>") != nil do
			$divCount = $divCount + 1
		end
		$divCount = $divCount -1

		#
		# Make sure the last div gets closed.
		#
		presTextHTML += "</div>";

		#
		# Fix all images to be on it's own after the slide div.
		#
		m = /\<p\>\<img src\=\"(.*)\" alt\=\"(.*)\" \/\>\<\/p\>/.match(presTextHTML)
		if m != nil
			postMatch = ""
			presTextHTML = ""
			while m != nil
				presTextHTML += m.pre_match
				presTextHTML += "<img src='#{m[1]}' class='#{m[2]}' />"
				postMatch = m.post_match
				m = /\<p\>\<img src\=\"(.*)\" alt\=\"(.*)\" \/\>\<\/p\>/.match(m.post_match)
			end
			presTextHTML += postMatch
		end
		presTextHTML += "<script> window.MaxSlideNum = #{$divCount}; </script>"

		#
		# Write the HTML to an index.html file in that directory.
		#
		target = open("#{$presDir}/index.html", 'w')
		target.truncate(0)
		target.write(presBegin + presTextHTML + presEnd)
		target.close

		#
		# Copy the CSS file to that directory and rename it to theme.css.
		#
		FileUtils.cp("#{pressBaseDir}/#{theme}.css",$presDir)
		File.rename("#{$presDir}/#{theme}.css","#{$presDir}/theme.css")

	   #
	   # Tell Dropzone what percentage is done.
	   #
	   $dz.percent((((index + 1)*100)/presNum).to_i)
	end

	#
	# Tell Dropzone that we are done.
	#
	$dz.finish("All Presentations Made.")

	# You should always call $dz.url or $dz.text last in your script. The below $dz.text line places text on the clipboard.
	# If you don't want to place anything on the clipboard you should still call $dz.url(false)
	$dz.url("file://#{$presDir}/index.html")
end

def clicked
	#
	# Allow the user to select a theme.
	#
	theme = "Basic"

	#
	# Show a list of themes.
	#
	qstr = "standard-dropdown --title \"Compress Files: Graphic Format\" --text \"What Theme?\" --items "
	themlist = []
	i = 0
	Dir.glob("*.css") { |filename|
		filename = File.basename(filename,".css")
		qstr += "\"#{filename}\" "
		themlist[i] = filename
		i += 1
	}
	button2, index =$dz.cocoa_dialog(qstr).split("\n")
	index = index.to_i
	theme = themlist[index]

	#
	# Set the selected theme.
	#
	$dz.save_value("theme", theme)

	#
	# Tell the user what they selected.
	#
	$dz.finish("You selected '#{theme}' for your theme.")
	$dz.url(false)
end

# Dropzone Action Info
# Name: GitHub
# Description: Easy clone a git repository. Hold Command key to select a destination folder.
# Handles: Text
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# OptionsNIB: ChooseFolder 
# SkipConfig: No
# Events: Dragged, Clicked
# KeyModifiers: Command
# Version: 1.0
# MinDropzoneVersion: 3.2.1

require 'uri'

def dragged

	modifier = ENV['KEY_MODIFIERS']
	folder = ENV['path']
	item = $items[0]

	if item =~ /\A#{URI::regexp}\z/

		url = URI.parse(item)
		projet_folder = url.path.split('/').last # Last path components
		projet_folder = projet_folder.gsub(/\.git$/,"") # Replace url ending with .git
		projet_folder = "Undefined" if projet_folder.empty? # If name undefined

		# Let user choose a destination directory
		if modifier == "Command"
			choosenfolder = $dz.cocoa_dialog("fileselect --title \"Select a clone directory\" --informative-text \"Select the directory where you want to Git to clone this project.\" --select-directories --debug --select-only-directories --string-output --with-directory \"#{folder}\" --no-newline")
			if !choosenfolder.empty?
				folder = choosenfolder
			end
		end

		absolute_path = File.join(folder,projet_folder)

		# Create a non existent directory
		if File.exists?(absolute_path) and File.directory?(absolute_path)
			puts "Project folder exists"
			idx = 1
			while File.exists?(absolute_path) do
				idx += 1
				newname = projet_folder+"-"+idx.to_s
				absolute_path = File.join(folder,newname)
			end
			projet_folder = newname
		end

		puts "Create directory at #{absolute_path}"
		Dir.mkdir(absolute_path)

		$dz.begin("Cloning git repository to #{projet_folder}.")

		# Clone git repository
		gitclone = `/usr/bin/git clone #{url} "#{absolute_path}" 2>&1`
		if ! $?.success?
			gitmessage = gitclone.split("\n")
			$dz.error("Git clone failed","Git failed to clone the repository:\n#{gitmessage[1]}")
			$dz.fail("Git failed to clone the repository.")
		end
		system("open #{absolute_path}")

		$dz.finish("Git project cloned to #{projet_folder}")
		$dz.url("#{absolute_path}")
	else
		$dz.fail("#{item} is not a valid URL.")
	end

end

def clicked
	folder = ENV['path']
	system("open #{folder}")
	$dz.url(false)
end

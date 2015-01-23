# Dropzone Action Info
# Name: Clone Git Repository
# Description: Drag the URL of a git repository onto this action and it will be cloned into the selected folder.\n\nHold the command key to select a different destination folder.
# Handles: Text
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# OptionsNIB: ChooseFolder 
# SkipConfig: No
# RunsSandboxed: No
# Events: Dragged, Clicked
# KeyModifiers: Command
# Version: 1.1
# MinDropzoneVersion: 3.2.1
# UniqueID: 1031

require 'uri'

def dragged

  modifier = ENV['KEY_MODIFIERS']
  folder = ENV['path']
  item = $items[0]

  if item =~ /\A#{URI::regexp}\z/

    url = URI.parse(item)
    project_folder = url.path.split('/').last # Last path components
    project_folder = project_folder.gsub(/\.git$/,"") # Replace url ending with .git
    project_folder = "Undefined" if project_folder.empty? # If name undefined

    # Let user select a folder to clone to
    if modifier == "Command"
      chosen_folder = $dz.cocoa_dialog("fileselect --title \"Select a folder to clone to\" --informative-text \"Select the folder where you want git to clone this project.\" --select-directories --debug --select-only-directories --string-output --with-directory \"#{folder}\" --no-newline")
      puts chosen_folder
      $dz.fail("You must select a folder") if chosen_folder.empty?
    end
    
    absolute_path = File.join(folder, project_folder)

    # Create directory if it doesn't already exist
    if File.exists?(absolute_path) and File.directory?(absolute_path)
      puts "Project folder exists"
      idx = 1
      while File.exists?(absolute_path) do
        idx += 1
        newname = project_folder + "-" + idx.to_s
        absolute_path = File.join(folder, newname)
      end
      project_folder = newname
    end

    puts "Create directory at #{absolute_path}"
    Dir.mkdir(absolute_path)

    $dz.begin("Cloning git repository to #{project_folder}")
    $dz.determinate(false)

    # Do the actual clone
    gitclone = `/usr/bin/gitd clone #{url} "#{absolute_path}" 2>&1`
    if ! $?.success?
      $dz.error("Git clone failed","Git failed to clone the repository:\n#{gitclone}")
      $dz.fail("Git failed to clone the repository.")
    end
    system("open #{absolute_path}")

    $dz.finish("Git project cloned to #{project_folder}")
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

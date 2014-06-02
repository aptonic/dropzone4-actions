# Dropzone Action Info
# Name: Bundle Script
# Description: Converts dropped .dropzone script files written for Dropzone 2 into shiny new .dzbundle packages for Dropzone 3.\n\nYou must choose a destination folder for the bundle output. Very nice
# Handles: Files
# Events: Dragged
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: ChooseFolder
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.1
# MinDropzoneVersion: 3.0
# UniqueID: 1001

require "open-uri"
require "fileutils"

def dragged
  $dz.determinate(false)
  
  bundled_files_count = 0
  
  $items.each do |item|
    next unless File.extname(item) == '.dropzone'
    $dz.begin("Bundling #{File.basename(item)}...")
    if process_dropzone_script(File.read(item))
      bundled_files_count += 1
    end
  end
  
  if (bundled_files_count > 0)
    s = (bundled_files_count == 1 ? "" : "s")
    $dz.finish("Successfully bundled #{bundled_files_count} script#{s}")
    `open \"#{ENV['EXTRA_PATH']}\" 2>&1`
  else
    $dz.finish("Bundle failed. No valid .dropzone scripts found.")
  end
  
  $dz.url(false)
end

def process_dropzone_script(file_contents)
  if file_contents =~ /# Name: (.*)/
    
    original_name = $1    
    
    # Make bundle folder
    bundle_name = "#{original_name}.dzbundle"
    bundle_path = ENV['EXTRA_PATH'] + '/' + bundle_name
    
    if File.exist?(bundle_path)
      output = $dz.cocoa_dialog("yesno-msgbox --text \"Bundle Already Exists\" --informative-text \"Bundle named '#{bundle_name}' already exists at destination. Overwrite?\" --no-cancel --float")
      if output.to_i == 1
        FileUtils.rm_r(bundle_path)
      else
        return false
      end
    end
  
    FileUtils.mkdir(bundle_path)

    if file_contents =~ /# IconURL: (.*)/    
      # Retrieve icon
      begin
        icon_data = open($1).read
      rescue
        $dz.error("Error downloading icon for #{original_name}", "Failed to download icon at URL '#{$1}'\n\n#{$!}")
      end
      
      File.open("#{bundle_path}/icon.png", 'wb') do |fo|
        fo.write icon_data
      end
    end

    lines = file_contents.split("\n")
    newfile = File.open("#{bundle_path}/action.rb", 'w')
    wrote_extra_meta = false
    needs_meta_added = false
    lines.each_with_index do |line, n|
      needs_meta_added = (line.gsub!(/# Dropzone Destination Info/, "# Dropzone Action Info") != nil or needs_meta_added)
      if line =~ /# (.*):(.*)/
        line.gsub!(/NSFilenamesPboardType/, "Files")
        line.gsub!(/NSStringPboardType/, "Text")
      else
        if (n > 2 and not wrote_extra_meta and needs_meta_added)
          newfile << "# Version: 1.0\n# RunsSandboxed: Yes\n# MinDropzoneVersion: 3.0\n"
          wrote_extra_meta = true
        end
      end
      if (not line =~ /\#\!\/usr\/bin\/ruby/ and not line =~ /# IconURL: (.*)/ and not (n == 1 and line.strip == ""))
        newfile << line + "\n"
      end
    end

    newfile.close
    true
  else
    false
  end
end
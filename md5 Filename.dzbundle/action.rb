# Dropzone Action Info
# Name: md5 Filename
# Description: Renames any dragged file(s) to a random, eight-characters-long md5 string.
# Handles: Files
# Creator: Kolja Nolte
# URL: https://www.koljanolte.com
# Events: Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0.0
# MinDropzoneVersion: 3.0

def dragged
  require 'digest'

  puts $items.inspect

  file_path     = $items[0].to_s
  basename      = File.basename(file_path)
  new_file_name = nil
  counter       = 0

  unless File.exist?(file_path)
    $dz.finish("Error: The file \"#{basename}\" could not be found. The file was not renamed.")

    exit
  end

  $dz.begin("Start renaming #{basename}...")
  $dz.determinate(true)

  $items.each do |file_path_single|
    current_directory = File.dirname(file_path_single)
    md5               = Digest::MD5.file file_path_single
    md5               = md5.hexdigest[1..8]
    file_extension    = File.extname(file_path_single)
    new_file_name     = md5 + file_extension
    new_file_path     = current_directory + '/' + new_file_name

    $dz.percent(10)
    sleep(0.3)
    $dz.percent(50)
    sleep(0.1)
    $dz.percent(100)

    if File.rename(File.path(file_path_single), new_file_path)
      counter += 1
    end
  end

  text = "File \"#{basename}\" has been successfully renamed to \"#{new_file_name}\"."

  if counter > 1
    text = "#{counter} files have been successfully renamed."
  end

  $dz.finish(text)
  $dz.text(false)
end
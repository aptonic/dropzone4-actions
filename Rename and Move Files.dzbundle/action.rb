# Dropzone Action Info
# Name: Rename and Move Files
# Description: Allows you to rename and move dropped files to a specified folder. Hold down option while dragging to rename and copy.
# Handles: Files
# Creator: Stephen Millard
# URL: http://thouhtasylum.com
# OptionsNIB: ChooseFolder
# UseSelectedItemNameAndIcon: Yes
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 81512718

# ACTION: FILE(S) DRAGGED ONTO ICON
def dragged
  # Rsync will provide progress updates, so set action to show progress
  $dz.determinate(true)
  
  # Log if we are copying or moving
  bMove = true
  if ENV['OPERATION'] == "NSDragOperationCopy"
    strOperation = "Copying"
    bMove = false
  else
    strOperation = "Moving"
  end
  
  # Rename all passed in files
  astrFileRenamed = Array.new 
  for intIndex in 0 ... $items.size
  
    # Display dialog to rename file
    strPashuaConfig = "
    *.title = Rename File
    p.type = textfield
    p.label = File Name
    p.default = #{File.basename($items[intIndex])}
    "
    objResult = $dz.pashua(strPashuaConfig)
    
    # Useful for debugging
    puts objResult['p']
    puts $items[intIndex]
    puts File.dirname($items[intIndex])
    
    # Rename the file
    strRenamedFilePath = File.dirname($items[intIndex]) + "/" + objResult['p']
    File.rename($items[intIndex], strRenamedFilePath)
    
    # Add the new file path to an array
    astrFileRenamed.push(strRenamedFilePath)
  end
  
  # Move/copy files
  # Uses the new set of file paths in the array
  $dz.begin("#{strOperation} files...")
  Rsync.do_copy(astrFileRenamed, ENV['EXTRA_PATH'], bMove)
  finish_op = (bMove ? "Move" : "Copy")
  
  # Notification with option to open the file path
  last_component = ENV['EXTRA_PATH'].split('/').last.gsub(/^(.{30,}?).*$/m,'\1...')
  $dz.finish("Click here to open the '#{last_component}' folder")
  $dz.url(false)
end


# ACTION: ICON CLICKED
def clicked
  # Open the folder path this action is set to move/copy to
  escaped_path = ENV['EXTRA_PATH'].gsub(/["`$\\]/){ |s| '\\' + s }
  system("open \"#{escaped_path}\"")
end

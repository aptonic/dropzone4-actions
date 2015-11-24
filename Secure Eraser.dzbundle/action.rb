# Dropzone Action Info
# Name: Secure Eraser
# Description: Erase dropped files or directories using secure erase.
# Creator: Aptonic Software
# URL: http://aptonic.com
# Handles: Files
# Version: 1.0
# SkipConfig: Yes
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1035

def dragged
  output = $dz.cocoa_dialog("yesno-msgbox --text 'Do you REALLY want to delete the dropped items?' --no-cancel")
  if output.to_i == 1
    files = ($items.length > 1 ? "Files" : "File")
    files = "Directory" if $items.length == 1 and File.directory?($items[0])
    $dz.begin("Secure Erasing #{files}...")
    $dz.determinate(false)

    result = ""

    $items.each do |item| 
      if File.directory?(item)
        result = `srm -rv "#{item}"`
      else
        result = `srm -v "#{item}"`
      end
    end
    
    puts result
    
    if not (result =~ /done/ or result =~ /removing/)
      $dz.fail("See the Dropzone debug console for details.")
    else
      $dz.finish("#{files} erased successfully.")
      $dz.url(false)
    end
  end
end

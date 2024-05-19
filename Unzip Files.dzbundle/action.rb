# Dropzone Action Info
# Name: Unzip Files
# Description: This action unzips zip files to the directory the zip file is in. Keeps the original zip file.
# Handles: Files
# Creator: Aptonic Software
# URL: https://aptonic.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: No
# UniqueID: 4631512
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
    $dz.determinate(false)
    total = $items.count

    $dz.begin("Unzipping #{$items.count} file(s)...")
    
    for $item in $items
      dir = File.dirname($item)
      `/usr/bin/unzip -n "#{$item}" -d "#{dir}" -x __MACOSX/\*`
    end

    $dz.finish("Unzipping Completed")
    $dz.url(false)
end

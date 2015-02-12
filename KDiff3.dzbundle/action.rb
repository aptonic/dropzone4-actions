# Dropzone Action Info
# Name: KDiff3
# Description: Drag 2 or 3 files or folders to diff them with KDiff3. Hold Command key (⌘) to merge the items.
# Creator: Eric W. Wallace
# URL: http://www.ewall.org/
# Handles: Files
# Events: Clicked, Dragged
# KeyModifiers: Command
# SkipConfig: Yes
# OptionsNIB: ChooseApplication
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def findApp
  if ENV["path"] == ""
    # not configured, so let's try the default location
    app = '/Applications/kdiff3.app/Contents/MacOS/kdiff3'
  else
    # is configured, build path to actual executable
    app = ENV["path"] + '/Contents/MacOS/kdiff3'
  end

  unless FileTest.executable?(app)
    $dz.fail('Cannot open KDiff3. Please confirm it is installed and configure the package with the correct location.')
    exit
  end

  return app
end

def dragged
  $dz.begin("Opening KDiff...")

  if $items.size < 2
    $dz.fail "We can compare only 2 or 3 items. Have you considered stashing files or folders in the Drop Bar, then dragging the items as group?"
    exit
  elsif $items.size > 3
    $dz.finish "Sorry, but we can compare no more than 3 items (files or directories)."
  end

  if ENV["KEY_MODIFIERS"] == "Command"
    $items.push('-m') # add flag to merge
  end

  unless system(findApp(), *$items)
    $dz.fail('Error opening KDiff3')
  end

  $dz.url(false)
end

def clicked
  $dz.begin("Opening KDiff...")

  unless system(findApp(), *$items)
    $dz.fail('Error opening KDiff3')
  end
  $dz.url(false)
end
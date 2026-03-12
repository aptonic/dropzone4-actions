# Dropzone Action Info
# Name: Annotate with CleanShot X
# Description: Drag images to annotate in CleanShot X.\n\nClick to capture area; hold ⌘ and click for fullscreen, hold ⌥ and click for window.\n\nRequires CleanShot X to be installed.
# Handles: Files
# Creator: Brett Terpstra
# URL: http://brettterpstra.com
# KeyModifiers: Command, Option
# Events: Clicked, Dragged
# SkipConfig: Yes
# RunsSandboxed: Yes
# UniqueID: 23455
# Version: 1.0
# MinDropzoneVersion: 3.0

require 'shellwords'

def dragged
  $dz.begin("Opening in CleanShotX...")
  $dz.determinate(true)
  $items.each do |file_path|
    `open "cleanshot://open-annotate?filepath=#{file_path}"`
  end

  $dz.finish("Image opened")
  $dz.url(false)
end

def clicked
  if ENV['KEY_MODIFIERS'] == 'Command'
     `open "cleanshot://capture-fullscreen?action=annotate"`
  elsif ENV['KEY_MODIFIERS'] == 'Option'
    `open "cleanshot://capture-window?action=annotate"`
  else
    `open "cleanshot://capture-area?action=annotate"`
  end
end

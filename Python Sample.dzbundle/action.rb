# Dropzone Action Info
# Name: Python Sample
# Description: Sample action using Python scripts.
# Handles: Files
# Creator: BlahGeek
# URL: http://blog.blahgeek.com
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.1
# MinDropzoneVersion: 3.0

def action(type)
  ENV["runner_path"] = $runner_path

  dirname = File.dirname(File.expand_path(__FILE__))
  script = File.join(dirname, "action.py")

  puts "Calling python script: #{script} #{type}"
  exec("python", script, type, *$items)
end

def dragged
  action("dragged")
end
 
def clicked
  action("clicked")
end

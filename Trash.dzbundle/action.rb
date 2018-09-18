# Dropzone Action Info
# Name: Trash
# Description: An action to throw items into the trash if Finder is running. Otherwise,
#                     it simply deletes them using the command line.
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  #
  # Begin the action.
  #
  $dz.begin("Trashing...")

  #
  # Below line switches the progress display to determinate mode so we can show progress
  #
  $dz.determinate(true)

  #
  # Below lines tell Dropzone to update the progress bar display and cycle through
  # each item dropped onto the action.
  #
  $dz.percent(1)
  count = $items.count
  index = 0
  $items.each {|file|
    #
    # Delete the file using the trash utility from Homebrew if Finder is running. Otherwise,
    # just delete it with the rm command.
    #
    finderR = `./finderRunning`
    if finderR =~ /not running/ then
        `rm -Rf "#{file}"`
    else
    	`./trash "#{file}"`
	end

    #
    # Tell Dropzone what percentage is done.
    #
    index = index + 1
    $dz.percent((((index + 1)*100)/count).to_i)
  }

  #
  # Show the user that the task is done.
  #
  $dz.finish("Task Complete")
  $dz.url(false)
end

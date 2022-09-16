# Dropzone Action Info
# Name: PDF Separate
# Description: This will take a PDF file and separate the pages using the HomeBrew installation of pdfseparate from the poppler library.
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Clicked, Dragged
# KeyModifiers: 
# SkipConfig: Yes
# RunsSandboxed: Yes
# Version: 1.0.0
# MinDropzoneVersion: 3.0

def dragged
  $dz.begin("Running PDFSeparate...")
  numitems = $items.count
  pdfDir = defined?( ENV['pdfDir'] ) ? ENV['pdfDir'] : "emails"
  $dz.save_value("pdfDir", pdfDir)
  progloc = defined?( ENV['progloc'] ) ? ENV['progloc'] : "/opt/homebrew/bin/pdfseparate"
  $dz.save_value("progloc", progloc)

  #
  # Below line switches the progress display to determinate mode so we can show progress
  #
  $dz.determinate(true)
  $dz.percent(1)
  
  #
  # Index over all of the given presentations.
  #
  for index in 0 ... numitems
    #
    # Get the note text.
    #
    file = $items[index]
    itemDir = File.dirname(file)
    
    #
    # Create the subdirectory if it doesn't exist.
    #
    if ! File.directory?("#{itemDir}/#{pdfDir}") then
      Dir.mkdir "#{itemDir}/#{pdfDir}"
    end

    #
    # Split the PDF file
    #
    `#{progloc} '#{file}' '#{itemDir}/#{pdfDir}/%d.pdf'`
    
    #
    # Update the percentage done.
    #
    $dz.percent((index/numitems)*100)
  end

  #
  # The below line tells Dropzone to end with a notification 
  # center notification with the text "Splitting Up Complete".
  #
  $dz.finish("Splitting Up Complete")
  
  # You should always call $dz.url or $dz.text last in your script. The below $dz.text line places text on the clipboard.
  # If you don't want to place anything on the clipboard you should still call $dz.url(false)
  $dz.url(false)
end

def clicked
    #
    # Get the subdirectory name from the environment.
    #
    pdfDir = defined?( ENV['pdfDir'] ) ? ENV['pdfDir'] : "emails"
    
    #
    # Get the directory to split the files into.
    #
    pdfDir = $dz.inputbox("PDF Separate", "What subdirectory name to use?")

    #
    # Set the directory name.
    #
    $dz.save_value("pdfDir", pdfDir)

    #
    # Get the location of the program.
    #
    progloc = defined?( ENV['progloc'] ) ? ENV['progloc'] : "/opt/homebrew/bin/pdfseparate"
    
    #
    # Get the program location from the user.
    progloc = $dz.inputbox("PDF Separate","Where is the program?")
    
    #
    # Save the program's location.
    #
    $dz.save_value("progloc", progloc)

    #
    # Tell the user what they selected.
    #
    $dz.finish("The output directory is '#{pdfDir}'")
    $dz.url(false)
end

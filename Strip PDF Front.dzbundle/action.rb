# Dropzone Action Info
# Name: Strip PDF Front
# Description: This actions takes PDF files, copies out the front cover picture, and scales it to the given size and the type given. Set the width and extension by clicking on the action. It uses the ImageMagick programs and the XPDF programs. Both are installable using HomeBrew. "brew install imagemagick" and "brew install xpdf".
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  # Get the routines global variables.
  $size = defined?( ENV['image_width'] ) ? ENV['image_width'] : 400
  $ext = defined?( ENV['image_ext'] ) ? ENV['image_ext'] : 'jpg'

  #
  # Get the total number of pdf files.
  #
  total = $items.count

  $dz.begin("Working on #{total} PDFs...")

  # Below line switches the progress display to determinate mode so we can show progress
  $dz.determinate(true)

  #
  # Create the temporary directory for the originals.
  #
  tmpDir = File.dirname($items[0]) + "/images"
  if ! File.directory?(tmpDir)
    #
    # Directory does not exist! Create it!
    #
    FileUtils.mkdir_p(tmpDir)
  end


  #
  # Index over all of the given images.
  #
  for index in 0 ... total
    filename = File.basename($items[index],".pdf")

    `/usr/local/bin/pdfimages -f 1 -l 1 '#{$items[index]}' '#{tmpDir}/#{filename}'`

    #
    # Convert the image file.
    #
    `/usr/local/bin/convert  -background white -quality 80% -alpha background -alpha off +dither -colors 512 -flatten -transparent none -resize #{$size} \"#{tmpDir}/#{filename}-0000.ppm\" \"#{tmpDir}/#{filename}#{$ext}\";`

    FileUtils.rm "#{tmpDir}/#{filename}-0000.ppm"

    #
    # Tell Dropzone what percentage is done.
    #
    $dz.percent((((index + 1)*100)/total).to_i)

    #
    # Set the results string to finished.
    #
    result = "Finished those PDFs."
  end

  # The below line tells Dropzone to end with a notification center notification with the text "Task Complete"
  $dz.finish(result)
  $dz.text(false)
end

def clicked
  #
  # The clicked handler should get the size and extension to use and
  # save it in the configuration file. We will save data in the
  # ~/Library/Application Support/Dropzone/Destination Data/CompressFiles.txt
  #

  #
  # Set the default return string to the error condition.
  #
  result = "Sorry, you canceled out."

  #
  # Request the width of the graphic.
  #
  button1, width =$dz.cocoa_dialog('standard-inputbox --title "PDF Picture: Graphic Width" --e --informative-text "What width? "').split("\n")

  #
  # See if the user canceled out. Do not continue if they cancel.
  #
  if button1 != "2"
    #
    # Ask for the graphic file type to end up with.
    #
    button2, extnum =$dz.cocoa_dialog('standard-dropdown --title "PDF Picture: Graphic Format" --text "What Graphic Format?" --items ".jpg" ".png" ".gif" ').split("\n")

    #
    # See if the user canceled out. Do not continue if they cancel.
    #
    if button2 != "2"
      #
      # Change the dropdown number to a string.
      #
      case extnum.to_i
      when 0
        ext = ".jpg"
      when 1
        ext = ".png"
      when 2
        ext = ".gif"
      end

      #
      # Write the data file. Do not append, but delete and write fresh!
      #
      $dz.save_value("image_width", width)
      $dz.save_value("image_ext", ext)

      #
      # Tell the user by setting the return string to what the user gave.
      #
      result = "Size: #{width} px, Ext: #{ext}"

      #
      # Tell the user that it is done.
      #
      $dz.finish(result)

      #
      # Finish out the dropzone protocal. If you want a url in the clipboard, pass it
      # here. If you just want to copy text to the clipboard, use $dz.text() instead.
      # Either $dz.url() or $dz.text() has to be the last thing in the clicked method.
      #
      $dz.url(false)
    end
  end
end

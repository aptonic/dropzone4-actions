# Dropzone Action Info
# Name: Strip PDF from Zip
# Description: This actions takes zip files,  and removes the PDF. It will give the PDF the same name as the zip file and delete the zip file.
# Handles: Files
# Creator: Richard Guay
# URL: http://customct.com
# Events: Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0

def dragged
  #
  # Get the total number of zip files.
  #
  total = $items.count

  $dz.begin("Working on #{total} Zips...")

  # Below line switches the progress display to determinate mode so we can show progress
  $dz.determinate(true)

  #
  # Index over all of the given images.
  #
  for index in 0 ... total
    #
    # Get the name of the zip file.
    #
    filename = File.basename($items[index],".zip")

    #
    # Get the full path to the zip file
    #
    zipath = File.dirname($items[index])

    #
    # Unzip the pdf file inside the zip file without the internal zip path to the
    # location of the zip file. Keep the output split by ':' to get the name of the
    # pdf file with it's path. This only works if there is one pdf in the zip!
    #
    output = `/usr/bin/unzip -j -d "#{zipath}" "#{$items[index]}" "*.pdf"`.split(':')

    #
    # Rename the pdf file to the same as the basename of the zip.
    #
    File.rename(output[2].strip,"#{zipath}/#{filename}.pdf")

    #
    # Remove the zip file.
    #
    FileUtils.rm("#{$items[index]}", :force => true)

    #
    # Tell Dropzone what percentage is done.
    #
    $dz.percent((((index + 1)*100)/total).to_i)

    #
    # Set the results string to finished.
    #
    result = "Finished those Zip files!"
  end

  #
  # The below line tells Dropzone to end with a notification center
  # notification with the text "Task Complete"
  #
  $dz.finish(result)
  $dz.text(false)
end

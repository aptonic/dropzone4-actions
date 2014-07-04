# Dropzone Action Info
# Name: Print
# Description: Dropped files will be printed. If you have multiple printers, you will be prompted for which printer you wish to use.\n\nNote this action is intended as just a quick and dirty way to quickly print an image, PDF or office document. It is not intended to let you configure print settings and may not always format documents correctly.
# Handles: Files
# Events: Dragged
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.0
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1012

$printing_tmp_folder = "#{$dz.temp_folder}/Dropzone-Printing"

def dragged
  standard_types = ["pdf", "jpg", "jpeg", "gif", "bmp", "png", "tif", "tiff", "txt", "rtf"]
  rich_types = ["xlsx", "xls", "docm", "dotx", "dotm", "xlsm",  "doc", "docx", "ppt", "pptx", "pptm"]
  
  # Check for valid type
  $items.each do |item|
    ext = File.extname(item).downcase[1..-1]
    if not standard_types.include?(ext) and not rich_types.include?(ext)
      $dz.fail("Unsupported Type")
    end
  end
  
  printer = get_printer()
  if printer == "use_default_printer"
    printer_flag = ""
  else
    printer_flag = "-d #{printer}"
  end
  
  lp_output = ""
  lp_command = ""
  
  system("/bin/rm -rf \"#{$printing_tmp_folder}\"")
  
  # Process and print each item
  $items.each do |item|
    ext = File.extname(item).downcase[1..-1]
    if standard_types.include?(ext)
      lp_command = "lp #{printer_flag} \"#{item}\" 2>&1"
      lp_output = `#{lp_command}`
    else
      # Convert document to PDF with qlmanage
      pdf_output_file = make_pdf(item)
      lp_command = "lp #{printer_flag} \"#{pdf_output_file}\" 2>&1"
      lp_output = `#{lp_command}`
    end
    
    if lp_output =~ /Error/
      $dz.error("Printing Error", "The lp command was called with #{lp_command} and returned " + lp_output)
    end
  end

  $dz.finish("Printing...")
  $dz.url(false)
end

def get_printer
  output = `lpstat -v 2>&1`
  if output =~ /No destinations added/
    $dz.fail("No Printers Available")
  end
    
  lpstat_output = output.split("\n")
  printers = ""
  return "use_default_printer" if lpstat_output.length == 1
  lpstat_output.each {|printer| printers = printers + " \"" + printer.split(" ")[2].gsub("_", " ")[0..-2] + "\""}
  s = ($items.length > 1 ? "s" : "")
  result = $dz.cocoa_dialog("dropdown --title \"Print #{$items.length} Item#{s}\" --text \"Select Printer:\" --items #{printers} --button1 \"OK\" --button2 \"Cancel\" --string-output")
  output_split = result.split("\n")
  
  if output_split[0] == "Cancel"
    $dz.fail("Cancelled")
  else
    return output_split[1].gsub(" ", "_")
  end
end

def make_pdf(path)
  Dir.mkdir($printing_tmp_folder) unless File.exists?($printing_tmp_folder)
  file = File.basename(path)
  puts `qlmanage -p -o "#{$printing_tmp_folder}" "#{path}"`
  if File.exists?("#{$printing_tmp_folder}/#{file}.qlpreview/Preview.html")
    a = File.read("#{$printing_tmp_folder}/#{file}.qlpreview/Preview.html") 
    b = a.gsub('<div class="PageStyle">',"").gsub('{background:#ACB2BB;}','')
    File.open("#{$printing_tmp_folder}/qlmanage-doc2pdf-tmp.html","w") {|f| f << b}
    output_filename = "#{$printing_tmp_folder}/#{file}.pdf"
    `/usr/sbin/cupsfilter \"#{$printing_tmp_folder}/qlmanage-doc2pdf-tmp.html\" > \"#{output_filename}\" 2> /dev/null`
    return output_filename
  else
    $dz.error("PDF Creation Error", "The generated preview file #{$printing_tmp_folder}/#{file}.qlpreview/Preview.html could not be found.")
  end
end

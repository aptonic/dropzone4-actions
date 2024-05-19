# Dropzone Action Info
# Name: Print
# Description: Dropped files will be printed. If you have multiple printers, you will be prompted for which printer you wish to use.\n\nNote this action is intended as just a quick and dirty way to quickly print an image, PDF, Pages or MS Office document. It is not intended to let you configure print settings.
# Handles: Files
# Events: Dragged
# Creator: Aptonic Software
# URL: http://aptonic.com
# Version: 1.4
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1012


$printing_tmp_folder = "#{$dz.temp_folder}/Dropzone-Printing"

def dragged
  standard_types = ["pdf", "jpg", "jpeg", "gif", "bmp", "png", "tif", "tiff", "txt", "rtf"]
  rich_types = ["xlsx", "xls", "docm", "dotx", "dotm", "dot", "xlsm",  "doc", "docx", "ppt", "pptx", "pptm", "pages"]
  
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
  
  # Process and print each item
  $items.each do |item|
    ext = File.extname(item).downcase[1..-1]
    if standard_types.include?(ext)
      lp_command = "lp #{printer_flag} \"#{item}\" 2>&1"
      lp_output = `#{lp_command}`
      
      if lp_output =~ /Error/
        $dz.error("Printing Error", "The lp command was called with #{lp_command} and returned " + lp_output)
      end
    else
      # Open the relevant app with AppleScript, print the file and quit
      if ["xlsx", "xls", "xlsm"].include?(ext)
        $dz.error("Microsoft Excel Printing", "Printing from Excel is not available currently as Excel does not support printing via AppleScript.")
        #run_app_and_print(printer, "Microsoft Excel", "sheet", item, true)
      elsif ["ppt", "pptx", "pptm"].include?(ext)
        run_app_and_print(printer, "Microsoft PowerPoint", "presentation", item, true)
      elsif ["docm", "dotx", "dot", "dotm", "doc", "docx"].include?(ext)
        run_app_and_print(printer, "Microsoft Word", "document", item, true)
      elsif ["pages"].include?(ext)
        run_app_and_print(printer, "Pages", "document", item, false)
      end
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
  printer_options = ""
  printers = []
  lpstat_printers = []
  return "use_default_printer" if lpstat_output.length == 1
  
  lpstat_output.each {|printer| 
    printer_friendly_name = printer.split(" ")[2].gsub("_", " ")[0..-2]
    printers << printer_friendly_name
    lpstat_printers << printer.split(" ")[2][0..-2]
    printer_options += "p.option = " + printer_friendly_name + "\n"
  }
  
  s = ($items.length > 1 ? "s" : "")
  
  # Get default printer
  d = ""
  output = ""
  output = `lpstat -d 2>&1`
  d = output.split(" ")[3].gsub("_", " ")

  # Added p.default to select the default printer
  printer_select_config = "
  *.title = Print #{$items.length} Item#{s}
  p.type = popup
  p.label = Select Printer:
  p.width = 310
  p.default = #{d}
  #{printer_options}
  cb.type = cancelbutton
  "

  result = $dz.pashua(printer_select_config)
  
  if result['cb'] == "1"
    $dz.fail("Cancelled")
  else
    selected_lpstat_printer = ""
    printers.each_with_index {|printer,index|
      if (result['p'].gsub(" ", "") == printer.gsub(" ", ""))
        selected_lpstat_printer = lpstat_printers[index]
        break
      end
    }
    
    return selected_lpstat_printer
  end
end

def run_app_and_print(printer, app_name, item_name, path, is_office)
  path.gsub!("\"", "\\\"")
  printer.gsub!("\"", "\\\"")
  printer_applescript = (printer == "use_default_printer" ? "" : "target printer:\"#{printer}\", ")
  
  if is_office
    # MS broke AppleScript and passing properties are no longer a thing, apparently
    print_cmd_applescript = "print the front #{item_name} without print dialog"
  else
    print_cmd_applescript = "print the front #{item_name} with properties {#{printer_applescript}copies:1}"
  end
  
result=`osascript -so <<END
tell application "#{app_name}"
	open POSIX file "#{path}"
	#{print_cmd_applescript}
	quit
end tell
END`
  puts result
  $dz.error("Failed to Print Document", "Error printing document.\n\nThis may be because '#{app_name}' cannot be found. Check the debug console for more info.") if result =~ /error/
end
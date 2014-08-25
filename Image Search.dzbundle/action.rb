# Dropzone Action Info
# Name: Image Search
# Description: Dropped images will be searched for using Google Image Search.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# Events: Dragged, Clicked
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 1022

require 'curl_uploader_mod'

def dragged
  $dz.determinate(false)
  
  allowed_exts = ["jpg", "jpeg", "gif", "tif", "tiff", "png", "bmp"]
  
  # Check only supported types were dragged
  $items.each do |item|
    filename = File.basename(item)
    ext = File.extname(item).downcase[1..-1]  
    $dz.fail("Only image files are supported") if not allowed_exts.include?(ext)
  end

  uploader = CurlUploaderMod.new
  uploader.upload_url = "https://www.google.com/searchbyimage/upload"
  uploader.file_field_name = "encoded_image"
  uploader.output_start_token = "<HTML>"
  uploader.expects_json_output = false
  
  results = uploader.upload($items)
  
  results.each do |result|
    check_upload_output_valid(result)
    extracted_url = /<A HREF=\"(.*)\"/.match(result[:output])[1]
    system("open \"#{extracted_url}\"")
  end
  
  $dz.finish("Search Complete")
  $dz.url(false)
end

def check_upload_output_valid(result)
  final_result = result[:output]
  if result[:curl_output_valid] and final_result =~ /<A HREF=/
    return true
  else
    error_message = final_result
    $dz.error("Error searching for image", "Uploader output:\n\n#{error_message}")
  end
end

def clicked
  system("open https://www.google.com/imghp")
end
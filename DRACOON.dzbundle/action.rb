# Dropzone Action Info
# Name: DRACOON
# Description: Upload a file to DRACOON and create a Download Share (URL will be placed in clipboard). Holding 'Command' (⌘) or 'Option' (⌥) will expire the uploaded file and its Download Share after 14 days, 'Control' (^) or 'Option' (⌥) will allow you to set a password for the Download Share. Holding 'Shift' (⇧) just uploads the file without sharing it. Clicking on this Action copies the latest Share Link to the clipboard.\nIcon is property of DRACOON GmbH.
# Handles: Files
# Creator: Florian Scheuer
# URL: https://github.com/F-Pseudonym/dracoon-for-dropzone
# Events: Dragged, Clicked
# KeyModifiers: Command, Control, Option, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# OptionsNIB: ExtendedLogin
# Version: 2.0.2
# MinDropzoneVersion: 3.0
# UniqueID: 3920135319837973180911208394894


require 'Date'
require 'Dracoon'
require 'erb'

DEFAULT_PATH = "DRACOON for Dropzone" #if no remote path is set in config
DEFAULT_VALIDITY = 14 #days


def dragged  

  server = ENV["server"]
  unless server.start_with?("http://") || server.start_with?("https://")
    server = "https://" + server
  end

  begin
    dracoon = Dracoon.new server
  rescue => e
    $dz.fail($!)
  end
      
 $dz.begin("Starting Preparations")
 $dz.determinate(true)
  
  
  # Determinate Password
  share_password = nil
  message = '"Choose your password:"'
  if ENV['KEY_MODIFIERS'] == 'Option' || ENV['KEY_MODIFIERS'] == 'Control'

    while share_password == nil do
      config ="
      pw.type = password
      pw.label = Please enter the password to protect the share.
      cancel.type = cancelbutton
      "
      result = $dz.pashua(config)
     
      if result['cancel'] == "1"
        $dz.fail("Canceled by user.")
      end
      
      share_password = result['pw']

      begin
        unless dracoon.check_password_compliance share_password
          message = '"Please chose a valid password!"'
          $dz.alert("Invalid password.", "The password you have chosen does not comply with the password policy.")
          share_password = nil
        end
      rescue
        $dz.fail("Error checking password compliance. Please check console for debug info.")
      end
    end

  end

  $dz.percent(5)
  $dz.begin("Selecting target location")

  # Determine Container ID for storage location
  if ENV["remote_path"] != nil
    full_path = ENV["remote_path"]
  else
    # prepare default path in home room (if applicable)
    homeroom_path = dracoon.get_homeroom_path
    if homeroom_path == nil
      full_path = DEFAULT_PATH
    else
      full_path = "#{homeroom_path}/#{DEFAULT_PATH}"
    end
  end

  if full_path.start_with?("/")
    full_path = full_path.slice(1,full_path.size)
  end
  if full_path.end_with?("/")
    full_path = full_path.slice(0,full_path.size-1)
  end

  $dz.save_value('remote_path', full_path)

  path = full_path.split('/')
  container_id = 0
  
  
  path.each do |name|
    begin
      node = dracoon.get_node_by_name name, container_id
    rescue
      $dz.fail("Error retrieving Folder info. Please check console for debug info.")
    end

    if node != nil
      container_id = node["id"]
    else
      #create container
      if container_id == 0
        begin
          node = dracoon.create_room name
          container_id = node["id"]
        rescue
          $dz.fail("Error creating Data Room. Please check console for debug info.")
        end
      else
        begin
          node = dracoon.create_folder name, container_id
          container_id = node["id"]
        rescue
          $dz.fail("Error creating folder. Please check console for debug info.")
        end
      end
      
    end
  end
  
  if container_id == nil
    $dz.fail("Container error!")
  end
  
  # Addtional folder if more than 1 file
  if $items.count > 1
    name = DateTime.now.strftime('%FT%H-%M-%S.%L')
    begin
      node = dracoon.create_folder name, container_id
    rescue
      $dz.fail("Error creating folder. Please check console for debug info.")
    end
    container_id = node["id"]
    container_name = node["name"]
  end
  
  $dz.percent(10)
  

  # calculate expiry date
  if ENV['KEY_MODIFIERS'] == 'Command' || ENV['KEY_MODIFIERS'] == 'Option'
    expiryDate = DateTime.now + DEFAULT_VALIDITY
  else
    expiryDate = nil
  end


  # Upload file(s)
  files = $items
  file_id = 0
  file_name = nil
  i = 0

  files.each do |file|
    i = i + 1
    file_name = file.rpartition('/').last

    # Upload File
    begin
      $dz.begin("Uploading #{file_name}")
      file_info = dracoon.upload_file File.new(file), container_id, expiryDate
    rescue
      $dz.fail("Error uploading file. Please check console for debug info.")
    end

    if file_info == nil
      $dz.fail("Upload failed.")
    end

    file_id = file_info["id"]
    $dz.percent((i * ((90 - 10) / $items.count )) + 10)
  end


  # Share only if Shift is not pressed
  unless ENV["KEY_MODIFIERS"] == 'Shift'

    access_key = nil

    # Determine ID to share and name
    if $items.count > 1
      id = container_id
      share_name = container_name
    else
      id = file_id
      share_name = file_name
    end

    # Create share link
    begin
      $dz.begin("Creating Share Link")
      share = dracoon.create_download_share id, share_password, expiryDate
      access_key = share["accessKey"]
    rescue
      $dz.fail("Error creating Share Link. Please check console for debug info.")
    end

    if access_key == nil
      $dz.fail("Error sharing file: No Access Key was provided")
    end

    share_link = share["link"]
    $dz.save_value('last_share_link', share_link)

  end

  $dz.percent(95)

  # Finish
  $dz.finish("Success!")
  $dz.text(share_link)

end


 
def clicked
  share_link = ENV['last_share_link']

  if share_link == nil
    $dz.fail("No Share Link available.")
  else
    $dz.finish("Last Share Link copied to clipboard.")
    $dz.text(share_link)
  end
end

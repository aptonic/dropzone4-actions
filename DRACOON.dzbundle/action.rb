# Dropzone Action Info
# Name: DRACOON
# Description: Upload a file to DRACOON and create a Download Share (URL will be placed in clipboard). Holding 'Command' (⌘) or 'Option' (⌥) will expire the uploaded file and its Download Share after 14 days, 'Control' (^) or 'Option' (⌥) will allow you to set a password for the Download Share. Holding 'Shift' (⇧) just uploads the file without sharing it. Clicking on this Action copies the latest Share Link to the clipboard.\nIcon is property of DRACOON GmbH.
# Handles: Files
# Creator: Florian Scheuer
# URL: https://github.com/F-Pseudonym/dropzone-share-with-dracoon
# Events: Dragged, Clicked
# KeyModifiers: Command, Control, Option, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# OptionsNIB: ExtendedLogin
# Version: 1.8
# MinDropzoneVersion: 3.0
# UniqueID: 3920135319837973180911208394894


require 'Date'
require 'dracoon'

DEFAULT_PATH = "DRACOON for Dropzone" #if no remote path is set in config
DEFAULT_VALIDITY = 14 #days


def dragged  

  server = ENV["server"]
  unless server.start_with?("http://") || server.start_with?("https://")
    server = "https://" + server
  end

  dracoon = Dracoon.new server

      
  $dz.begin("Starting Preparations")
  $dz.determinate(true)
  
  
  # User log-on
  begin
    auth_token = dracoon.login ENV["username"], ENV["password"]
  rescue
    $dz.fail("Login error. Please check console for debug info.")
  end
  

  if auth_token == "" or auth_token == nil
    $dz.fail("Login error. No token provided.")
  end
  

  # Determinate Password
  share_password = nil
  message = '"Choose your password:"'
  if ENV['KEY_MODIFIERS'] == 'Option' || ENV['KEY_MODIFIERS'] == 'Control'

    while share_password == nil do
      input = $dz.cocoa_dialog('standard-inputbox --title "Password for Share Link" --informative-text '+message+' --no-show --no-newline')
      button, share_password = input.split("\n")

      if button == "2"
        $dz.fail("Canceled by user.")
      end
      
      begin
        unless dracoon.check_password_compliance share_password
          message = '"Please chose a valid password! (8+ characters, uppercase, lowercase, special chars)"'
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
    full_path = DEFAULT_PATH
  end
  
  if full_path.start_with?("/")
    full_path = full_path.slice(1,full_path.size)
  end
  if full_path.end_with?("/")
    full_path = full_path.slice(0,full_path.size-1)
  end
  
  path = full_path.split('/')
  container_id = 0
  path.each do |name|
    # Get Data Rooms to retrieve room_id
    begin
      nodes = dracoon.get_nodes_by_name name, container_id, depth_level = 0
    rescue
      $dz.fail("Error retrieving Folder info. Please check console for debug info.")
    end

    # Fetch room_id
    if nodes["range"]["total"] > 0
      
      containers = nodes["items"]
      containers.each do |container|
        if container["name"] == name
          container_id = container["id"]
        end
      end
      
    else    
      # Create Room/Folder
      if container_id == 0
        begin
          node = dracoon.create_room name
        rescue
          $dz.fail("Error creating Data Room. Please check console for debug info.")
        end
      else
        begin
          node = dracoon.create_folder name, container_id
        rescue
          $dz.fail("Error creating folder. Please check console for debug info.")
        end
      end
      container_id = node["id"]
    end
  end  
  
  if container_id == nil
    $dz.fail("Room error!")
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
      file_info = dracoon.upload_file File.new(file), container_id, expire_at = expiryDate
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
      share = dracoon.create_download_share id, share_name, share_password, false, expire_at = expiryDate
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

  
  # User logout
  begin
    dracoon.logout
  rescue
    $dz.fail("Error logging off. Please check console for debug info.")
  end
  
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

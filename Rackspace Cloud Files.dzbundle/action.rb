# Dropzone Action Info
# Name: Rackspace Cloud Files
# Description: Uploads files to a Rackspace Cloud Files account container.\n\nYou will be prompted for the region and container on your first upload. Click the action to change the configured container.
# Handles: Files
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: UsernameAPIKey
# Events: Dragged, Clicked
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 1014

require 'lib/fog'

def dragged
  $dz.determinate(false)
    
  $dz.begin("Connecting to Rackspace Cloud Files...")
  configureClient()

  $dz.begin("Getting container...")
  # Try to get remote container name from saved values
  remoteContainerName = ENV['container']

  # If not available, then read it and save it
  if remoteContainerName.to_s.strip.length == 0
    remoteContainerName = setContainer()
  end

  # Retrieve the directory that matches the container name
  remoteContainer = @client.directories.get(remoteContainerName)

  # If it doesn't exist, then create it and consider enabling CDN on it
  if(remoteContainer.nil?)
    enableCDN = (ENV['enableCDN'] == "true" ? true : false)
    enabledCDNMessage = enableCDN ? "enabled" : "disabled"
    $dz.begin("Adding new container with CDN #{enabledCDNMessage}...")
    
    remoteContainer = @client.directories.create(:key => remoteContainerName)
    remoteContainer.public = enableCDN
    remoteContainer.save
  end

  urls ||= Array.new

  # Upload each file to the cloud files endpoint
  $items.each do |file|
    urls << uploadFile(file, remoteContainer)
  end

  if urls.length == 1
    if urls[0].nil? or urls[0].to_s.strip.length == 0
      $dz.finish("No URL(s) were copied to clipboard, because CDN is disabled or no URL was returned!")
      $dz.url(false)
    else
      $dz.finish("URL is now on clipboard")
      $dz.url("#{urls[0]}")
    end
  elsif urls.length > 1
    mergedURLs = urls.join(" ")
    if mergedURLs.to_s.strip.length == 0
      $dz.finish("No URL(s) were copied to clipboard, because CDN is disabled or no URL was returned!")
      $dz.url(false)
    else
      $dz.finish("URLs are now on clipboard")
      $dz.text(mergedURLs)
    end
  end
    
end

def clicked
  $dz.determinate(false)

  setRegion()

  setContainer()

  $dz.finish("Selected region and container name were saved!")

  $dz.url(false)
end

def setRegion
  output = $dz.cocoa_dialog('dropdown --button1 "OK" --button2 "Cancel" --title "Rackspace region" --text "Which region do you want to use?" --items "Dallas-Fort Worth (DFW)" "Chicago (ORD)" "Northern Virginia (IAD)" "London (LON)" "Sydney (SYD)" "Hong Kong (HKG)"')
  button, regionIndex = output.split("\n")

  if button == "2"
    $dz.fail("Cancelled")
  end

  region = ""
  case regionIndex
  when "0"
    region = "DFW"
  when "1"
    region = "ORD"
  when "2"
    region = "IAD"
  when "3"
    region = "LON"
  when "4"
    region = "SYD"
  when "5"
    region = "HKG"
  end

  $dz.save_value('region', region)

  region
end

def setContainer
  # Get the container name
  output = $dz.cocoa_dialog('inputbox --button1 "OK" --button2 "Cancel" --title "Container name" --e --informative-text "In what container should the files be uploaded to? (will be created if it doesn\'t exist)"')
  
  button, remoteContainerName = output.split("\n")
  
  if button == "2"
    $dz.fail("Cancelled")
  end
  
  # Fail if no container name is entered
  if remoteContainerName.to_s.strip.length == 0
    $dz.fail("Container name cannot be empty!")
  elsif
    $dz.save_value('container', remoteContainerName)
  end
  
  # Get if CDN should be enabled on a new container or not
  output = $dz.cocoa_dialog('yesno-msgbox --no-cancel --title "Enable CDN" --e --text "Enable CDN on this new container?" --informative-text "If CDN is not enabled, then no URL will be copied to the clipboard when an upload completes."')
  
  enableCDNOption, nothing = output.split("\n")
  
  enableCDN = true
  if enableCDNOption == "2"
    enableCDN = false
  end
  
  $dz.save_value('enableCDN', enableCDN)
  
  remoteContainerName
end

def uploadFile (filePath, directory)
  fileName = filePath.split(File::SEPARATOR).last
  file = directory.files.get(fileName)
  localFile = File.open(filePath)
  
  unless file.nil?
    # Delete the remote file, if it exists
    file.destroy
    file.save
  end
  
  $dz.begin("Uploading #{File.basename(fileName)} ...")
  file = directory.files.create(
    :key => fileName,
    :body => localFile
  )
                                    
  file.save
                                    
  file.public_url
end
    
def configureClient
  # Get the region from the local values
  region = ENV['region']
  
  # If not available, then read it and save it
  if region.to_s.strip.length == 0
    region = setRegion()
  end
  
  @client = Fog::Storage.new(
    :provider => 'rackspace',
    :rackspace_username => ENV['username'],
    :rackspace_api_key => ENV['api_key'],
    :rackspace_region => region
  )
end

require 'lib/fog'

class Rackspace
  def readRegion
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
  
  def readContainerName
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

    remoteContainerName
  end

  def readCDN
    # Get if CDN should be enabled on a new container or not
    output = $dz.cocoa_dialog('yesno-msgbox --no-cancel --title "Enable CDN" --e --text "Enable CDN on this new container?" --informative-text "If CDN is not enabled, then no URL will be copied to the clipboard when an upload completes."')
    
    enableCDNOption, nothing = output.split("\n")
    
    enableCDN = true
    if enableCDNOption == "2"
      enableCDN = false
    end
    
    $dz.save_value('enableCDN', enableCDN)

    enableCDN
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
      region = readRegion()
    end
    begin
      @client = Fog::Storage.new(
        :provider => 'rackspace',
        :rackspace_username => ENV['username'],
        :rackspace_api_key => ENV['api_key'],
        :rackspace_region => region
      ) 
    rescue Excon::Errors::Unauthorized
      $dz.error("Incorrect username and api key", "The username and the api key you configured seem to be incorrect! Please verify, correct them and retry!")
    end
  end

  def getRemoteContainer
    # Try to get remote container name from saved values
    remoteContainerName = ENV['container']

    # If not available, then read it and save it
    if remoteContainerName.to_s.strip.length == 0
      remoteContainerName = readContainerName()
    end

    remoteContainer = @client.directories.get(remoteContainerName)

    # If it's nil, then create a new one
    if(remoteContainer.nil?)
      enableCDN = getCDN()
      enabledCDNMessage = enableCDN ? "enabled" : "disabled"
      $dz.begin("Adding new container with CDN #{enabledCDNMessage}...")
      
      remoteContainer = createRemoteContainer(remoteContainerName, enableCDN)
    end

    remoteContainer
  end

  def getCDN
     # Try to get if CDN should be enabled from saved values
    enableCDNString = ENV['enableCDN']

    enableCDN = true
    # If not available, then read it and save it
    if enableCDNString.to_s.strip.length == 0
      enableCDN = readCDN()
    else
      enableCDN = (enableCDNString == "true" ? true : false)
    end

    enableCDN
  end

  def createRemoteContainer(remoteContainerName, enableCDN)
    remoteContainer = @client.directories.create(:key => remoteContainerName)
    remoteContainer.public = enableCDN
    remoteContainer.save

    remoteContainer
  end
end
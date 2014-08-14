require 'lib/fog'

class Rackspace
  def read_region
    output = $dz.cocoa_dialog('dropdown --button1 "OK" --button2 "Cancel" --title "Rackspace region" --text "Which region do you want to use?" --items "Dallas-Fort Worth (DFW)" "Chicago (ORD)" "Northern Virginia (IAD)" "London (LON)" "Sydney (SYD)" "Hong Kong (HKG)"')
    button, region_index = output.split("\n")
  
    if button == "2"
      $dz.fail("Cancelled")
    end
  
    region = ""
    case region_index
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
  
  def read_container_name
    # Get the container name
    output = $dz.cocoa_dialog('inputbox --button1 "OK" --button2 "Cancel" --title "Container name" --e --informative-text "In what container should the files be uploaded to? (will be created if it doesn\'t exist)"')
    
    button, remote_container_name = output.split("\n")
    
    if button == "2"
      $dz.fail("Cancelled")
    end
    
    # Fail if no container name is entered
    if remote_container_name.to_s.strip.length == 0
      $dz.fail("Container name cannot be empty!")
    elsif
      $dz.save_value('container', remote_container_name)
    end

    remote_container_name
  end

  def read_cdn
    # Get if CDN should be enabled on a new container or not
    output = $dz.cocoa_dialog('yesno-msgbox --no-cancel --title "Enable CDN" --e --text "Enable CDN on this new container?" --informative-text "If CDN is not enabled, then no URL will be copied to the clipboard when an upload completes."')
    
    enable_cdn_option, nothing = output.split("\n")
    
    enable_cdn = true
    if enable_cdn_option == "2"
      enable_cdn = false
    end
    
    $dz.save_value('enableCDN', enable_cdn)

    enable_cdn
  end

  
  def upload_file (file_path, directory)
    file_name = file_path.split(File::SEPARATOR).last
    file = directory.files.get(file_name)
    localFile = File.open(file_path)
    
    unless file.nil?
      # Delete the remote file, if it exists
      file.destroy
      file.save
    end
    
    $dz.begin("Uploading #{File.basename(file_name)} ...")
    file = directory.files.create(
      :key => file_name,
      :body => localFile
    )
                                      
    file.save
                                      
    file.public_url
  end
      
  def configure_client
    # Get the region from the local values
    region = ENV['region']
    
    # If not available, then read it and save it
    if region.to_s.strip.length == 0
      region = read_region()
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
    rescue RuntimeError
      $dz.error("Error while connecting to Rackpace", "There was an error while connecting to Rackpace. Please check that you have access to the chosen region with your account!")
    end
  end

  def get_remote_container
    # Try to get remote container name from saved values
    remote_container_name = ENV['container']

    # If not available, then read it and save it
    if remote_container_name.to_s.strip.length == 0
      remote_container_name = read_container_name()
    end

    remote_container = @client.directories.get(remote_container_name)

    # If it's nil, then create a new one
    if(remote_container.nil?)
      enable_cdn = get_cdn()
      enabledCDNMessage = enable_cdn ? "enabled" : "disabled"
      $dz.begin("Adding new container with CDN #{enabledCDNMessage}...")
      
      begin
        remote_container = create_remote_container(remote_container_name, enable_cdn)
      rescue Fog::Storage::Rackspace::BadRequest
        $dz.error("Error while creating container", "There was an error while creating the container. Please check that you have access to the chosen region with your account!")
      rescue RuntimeError
        $dz.error("Error while creating container", "There was an error while creating the container. Please check that you have access to the chosen region with your account!")
      end
    end

    remote_container
  end

  def get_cdn
     # Try to get if CDN should be enabled from saved values
    enable_cdn_string = ENV['enableCDN']

    enable_cdn = true
    # If not available, then read it and save it
    if enable_cdn_string.to_s.strip.length == 0
      enable_cdn = read_cdn()
    else
      enable_cdn = (enable_cdn_string == "true" ? true : false)
    end

    enable_cdn
  end

  def get_custom_domain
    ENV['domain']
  end

  def create_remote_container(remote_container_name, enable_cdn)
    remote_container = @client.directories.create(:key => remote_container_name)
    remote_container.public = enable_cdn
    remote_container.save

    remote_container
  end

  def read_custom_domain()
    # Get the container name
    output = $dz.cocoa_dialog('inputbox --button1 "OK" --button2 "Cancel" --title "Custom domain" --e --informative-text "Fill in below what custom domain should be used for the container (ex. \"images.domain.com\", leave empty if not needed)"')
    
    button, domain = output.split("\n")
    
    if button == "2"
      $dz.fail("Cancelled")
    end
    
    # Fail if no container name is entered
    if domain.to_s.strip.length > 0
      $dz.save_value('domain', domain)
    else
      $dz.save_value('domain', 'nil')
    end

    domain
  end
end
require 'lib/fog'

class Rackspace
  # SEGMENT_LIMIT = 5368709119.0
  SEGMENT_LIMIT = 1024 * 1024
  BUFFER_SIZE = Excon.defaults[:chunk_size] || 1024 * 1024

  def read_region
    output = $dz.cocoa_dialog('dropdown --button1 "OK" --button2 "Cancel" --title "Rackspace region" --text "Which region do you want to use?" --items "Dallas-Fort Worth (DFW)" "Chicago (ORD)" "Northern Virginia (IAD)" "London (LON)" "Sydney (SYD)" "Hong Kong (HKG)"')
    button, region_index = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
    end

    case region_index
      when '0'
        region = 'DFW'
      when '1'
        region = 'ORD'
      when '2'
        region = 'IAD'
      when '3'
        region = 'LON'
      when '4'
        region = 'SYD'
      when '5'
        region = 'HKG'
      else
        region = 'ORD'
    end

    $dz.save_value('region', region)

    region
  end

  def read_container_name
    # Get the container name
    output = $dz.cocoa_dialog('inputbox --button1 "OK" --button2 "Cancel" --title "Container name" --e --informative-text "In what container should the files be uploaded to? (will be created if it doesn\'t exist)"')

    button, remote_container_name = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
    end

    # Fail if no container name is entered
    if remote_container_name.to_s.strip.length == 0
      $dz.fail('Container name cannot be empty!')
    else
      $dz.save_value('container', remote_container_name)
    end

    remote_container_name
  end

  def read_cdn
    # Get if CDN should be enabled on a new container or not
    output = $dz.cocoa_dialog('yesno-msgbox --no-cancel --title "Enable CDN" --e --text "Enable CDN on this new container?" --informative-text "If CDN is not enabled, then no URL will be copied to the clipboard when an upload completes."')

    enable_cdn_option, nothing = output.split("\n")

    enable_cdn = true
    if enable_cdn_option == '2'
      enable_cdn = false
    end

    $dz.save_value('enableCDN', enable_cdn)

    enable_cdn
  end


  def upload_file (file_path, directory)
    file = File.open(file_path)

    url = ''
    unless file.nil?
      if file.stat.size > SEGMENT_LIMIT
        url = upload_large_file(file, directory)
      else
        url = upload_small_file(file, directory)
      end
    end

    url
  end

  def upload_small_file(file, directory)
    response = nil
    url = ''
    file_size = file.stat.size
    last_output = 0

    begin
      $dz.begin("Uploading #{File.basename(file.path)} ...")
      $dz.determinate(true)

      until file.eof?
        offset = 0

        response = @client.put_object(directory.key, File.basename(file.path), nil) do
          buf = file.read(BUFFER_SIZE).to_s
          offset += buf.size

          upload_percent = (offset.to_f/file_size * 100).to_i
          if last_output != upload_percent
            $dz.percent(upload_percent)
            $dz.determinate(false) if upload_percent == 100
          end

          last_output = upload_percent

          buf
        end
      end
    rescue Exception => e
      $dz.error('Error occurred while uploading file to Rackspace Cloud Files', e.message)
    end

    if response.status == 201
      url = determine_file_url(directory, file)
    else
      $dz.error('Error occurred while uploading file to Rackspace Cloud Files', response.status)
    end

    url
  end


  def upload_large_file(file, directory)
    segment_name = File.basename(file.path)
    file_size = file.stat.size

    segment = 0
    uploaded = 0
    last_output = 0

    begin
      $dz.begin("Uploading #{File.basename(file.path)} ...")
      $dz.determinate(true)

      until file.eof?
        segment += 1
        offset = 0

        # upload segment to cloud files
        segment_suffix = segment.to_s.rjust(10, '0')
        response = @client.put_object(directory.key, "#{segment_name}/#{segment_suffix}", nil) do
          if offset <= SEGMENT_LIMIT - BUFFER_SIZE
            buf = file.read(BUFFER_SIZE).to_s
            offset += buf.size
            uploaded += offset

            upload_percent = (uploaded.to_f/file_size * 100).to_i
            if last_output != upload_percent
              $dz.percent(upload_percent)
              $dz.determinate(false) if upload_percent == 100
            end

            last_output = upload_percent

            buf
          else
            ''
          end
        end

        if response.status != 201
          $dz.error('Error occurred while uploading file to Rackspace Cloud Files', response.status)
        end
      end
    rescue Exception => e
      $dz.error('Error occurred while uploading file to Rackspace Cloud Files', e.message)
    end

    @client.put_object_manifest(directory.key, segment_name, 'X-Object-Manifest' => "#{directory.key}/#{segment_name}/")

    determine_file_url(directory, file)
  end

  def determine_file_url(directory, file)
    url = ''
    if directory.public_url
      domain = get_custom_domain

      escaped_file_name = Fog::Rackspace.escape(File.basename(file.path), '/')
      if domain != nil and domain != 'nil'
        url = "http://#{domain}/#{escaped_file_name}"
      else
        url = "#{directory.public_url}/#{escaped_file_name}"
      end
    end

    url
  end

  def configure_client
    # Get the region from the local values
    region = ENV['region']

    # If not available, then read it and save it
    if region.to_s.strip.length == 0
      region = read_region
    end
    begin
      @client = Fog::Storage.new(
          :provider => 'rackspace',
          :rackspace_username => ENV['username'],
          :rackspace_api_key => ENV['api_key'],
          :rackspace_region => region
      )
    rescue Excon::Errors::Unauthorized
      $dz.error('Incorrect username and api key', 'The username and the api key you configured seem to be incorrect! Please verify, correct them and retry!')
    rescue RuntimeError
      $dz.error('Error while connecting to Rackpace', 'There was an error while connecting to Rackpace. Please check that you have access to the chosen region with your account!')
    end
  end

  def get_remote_container
    # Try to get remote container name from saved values
    remote_container_name = ENV['container']

    # If not available, then read it and save it
    if remote_container_name.to_s.strip.length == 0
      remote_container_name = read_container_name
    end

    remote_container = @client.directories.get(remote_container_name)

    # If it's nil, then create a new one
    if remote_container.nil?
      enable_cdn = get_cdn
      enabled_cdn_message = enable_cdn ? 'enabled' : 'disabled'
      $dz.begin("Adding new container #{remote_container_name} with CDN #{enabled_cdn_message}...")

      begin
        remote_container = create_remote_container(remote_container_name, enable_cdn)
      rescue Fog::Storage::Rackspace::BadRequest
        $dz.error('Error while creating container', 'There was an error while creating the container. Please check that you have access to the chosen region with your account!')
      rescue RuntimeError
        $dz.error('Error while creating container', 'There was an error while creating the container. Please check that you have access to the chosen region with your account!')
      end
    else
      enable_cdn = get_cdn
      enabled_cdn_message = enable_cdn ? 'Enabling' : 'Disabling'

      $dz.begin("#{enabled_cdn_message} CDN for the container #{remote_container_name}...")
      remote_container.public = enable_cdn
      remote_container.save
    end

    remote_container
  end

  def get_cdn
    # Try to get if CDN should be enabled from saved values
    enable_cdn_string = ENV['enableCDN']

    # If not available, then read it and save it
    if enable_cdn_string.to_s.strip.length == 0
      enable_cdn = read_cdn
    else
      enable_cdn = (enable_cdn_string == 'true' ? true : false)
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

  def read_custom_domain
    # Get the container name
    output = $dz.cocoa_dialog('inputbox --button1 "OK" --button2 "Cancel" --title "Custom domain" --e --informative-text "Fill in below what custom domain should be used for the container (ex. \"images.domain.com\", leave empty if not needed)"')

    button, domain = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
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
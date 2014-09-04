require 'lib/google/api_client'
require 'lib/google/api_client/auth/file_storage'
require 'lib/google/api_client/auth/installed_app'
require 'securerandom'

class Gdrive
  API_VERSION = 'v2'
  CACHED_API_FILE = "drive-#{API_VERSION}.cache"
  CREDENTIAL_STORE_FILE = 'oauth2.json'
  Folder = Struct.new(:title, :folder_id)

  def configure_client
    $dz.begin('Connecting to Google Drive...')

    unique_client_id = ENV['unique_client_id']
    if unique_client_id.nil? or unique_client_id.to_s.strip.length == 0
      unique_client_id = urlsafe_base64
      $dz.save_value('unique_client_id', unique_client_id)
    end

    temp_file_base_path = "#{$dz.temp_folder}/#{unique_client_id}"

    @client = Google::APIClient.new(:application_name => 'Dropzone 3 action for Google Drive',
                                    :application_version => '1.0.0')

    authorization = Signet::OAuth2::Client.new({
                                                    :authorization_uri => 'https://accounts.google.com/o/oauth2/auth',
                                                    :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
                                                    :client_id => ENV['client_id'],
                                                    :client_secret => ENV['client_secret'],
                                                    :refresh_token => ENV['refresh_token']
                                                })
    authorization.fetch_access_token!
    @client.authorization = authorization

    @drive = nil
    temp_cached_api_file = "#{temp_file_base_path}_#{CACHED_API_FILE}"
    if File.exists? temp_cached_api_file
      File.open(temp_cached_api_file) do |file|
        @drive = Marshal.load(file)
      end
    else
      @drive = @client.discovered_api('drive', API_VERSION)
      File.open(temp_cached_api_file, 'w') do |file|
        Marshal.dump(@drive, file)
      end
    end

  end

  def upload_file (file_path, folder_id)
    file_name = file_path.split(File::SEPARATOR).last
    $dz.begin("Uploading #{file_name} to Google Drive...")
    content_type = `file -Ib #{file_path}`.gsub(/\n/, "")


    file = @drive.files.insert.request_schema.new({
                                                      :title => file_name,
                                                      :mimeType => content_type,
                                                      :parents => [{:id => folder_id}]
                                                  })

    media = Google::APIClient::UploadIO.new(file_path, content_type)
    result = @client.execute(
        :api_method => @drive.files.insert,
        :body_object => file,
        :media => media,
        :parameters => {
            :uploadType => 'multipart',
            :alt => 'json'
        })

    unless result.success?
      $dz.error(result.error_message)
    end
  end

  def get_folders
    result = @client.execute(
        :api_method => @drive.files.list,
        :parameters => {
            :q => "'root' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        })

    # using an array and a struct to guarantee order
    folders = Array.new
    result.data['items'].each { |item|
      folders << Folder.new(item['title'], item['id'])
    }

    folders
  end

  def select_folder
    $dz.begin('What folder would you like to use?')
    folders = get_folders

    if folders.empty?
      folder_id = read_folder
    else
      folder_names = ''

      # check if there was a previously selected folder and if it's still in the folder list
      saved_folder_name = ENV['folder_name']
      index_saved_folder_name = folders.index { |x| x.title == saved_folder_name }
      no_saved_folder = (saved_folder_name.nil? or saved_folder_name.to_s.strip.length == 0 or index_saved_folder_name.nil?)

      # if there's a valid saved folder, then display it first and reorder array
      unless no_saved_folder
        folder_names = "#{folder_names} \"#{saved_folder_name}\" "
        folders.insert(0, folders.delete_at(index_saved_folder_name))
      end

      # arrange the list of folders, don't display the saved folder name again
      folders.each do |folder|
        unless !no_saved_folder and saved_folder_name == folder.title
          folder_names = "#{folder_names} \"#{folder.title}\" "
        end
      end

      output = $dz.cocoa_dialog("dropdown --button1 \"OK\" --button2 \"Cancel\"  --button3 \"New folder\" --title \"Select a folder\" --text \"In which folder would like to upload the file(s)?\" --items #{folder_names}")
      button, folder_index = output.split("\n")

      if button == '2'
        $dz.fail('Cancelled')
      end

      # if the user wants to create a new folder, or use one of the existing ones
      if button == '3'
        folder_id = read_folder
      else
        folder_index_int = Integer(folder_index)
        selected_folder = folders[folder_index_int]
        $dz.save_value('folder_name', selected_folder.title)
        folder_id = selected_folder.folder_id
      end
    end

    folder_id
  end

  def read_folder
    output = $dz.cocoa_dialog("standard-inputbox --button1 \"OK\" --button2 \"Cancel\" --title \"Create new folder\" --informative-text \"Enter the name of the new folder, where the file(s) will be uploaded:\"")
    button, folder_name = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
    end

    if folder_name.to_s.strip.length == 0
      $dz.fail('You need to choose a folder!')
    end

    folder_id = create_new_folder(folder_name)
    $dz.save_value('folder_name', folder_name)

    folder_id
  end

  def create_new_folder(folder_name)
    $dz.begin("Creating new folder #{folder_name}...")
    content_type = 'application/vnd.google-apps.folder'

    file = @drive.files.insert.request_schema.new({
                                                      :title => folder_name,
                                                      :mimeType => content_type
                                                  })
    result = @client.execute(
        :api_method => @drive.files.insert,
        :body_object => file
    )

    unless result.success?
      $dz.error(result.error_message)
    end

    result.data['id']
  end

  # copied it from http://softover.com/UUID_in_Ruby_1.8
  def urlsafe_base64(n=nil, padding=false)
    s = [SecureRandom.random_bytes(n)].pack('m*')
    s.delete!("\n")
    s.tr!('+/', '-_')
    s.delete!('=') unless padding
    s
  end
end
require 'google/apis/drive_v2'

class Gdrive
  Drive = Google::Apis::DriveV2
  Folder = Struct.new(:title, :folder_id)

  def configure_client
    $dz.begin('Connecting to Google Drive...')
    
    @drive = Drive::DriveService.new
    @drive.authorization = get_authorization
  end

  def get_authorization
    if ENV['expires_at'].nil? or ENV['access_token'].nil?
      $dz.error('Redo authorization', 'The authorization data is not complete. Please redo the authorization from the action\'s Edit screen.')
    end

    token_expiration_time_ms = ENV['expires_at'].to_i
    if token_expiration_time_ms > Time.now.to_i
      authorization = Signet::OAuth2::Client.new({
                                                     :authorization_uri => 'https://accounts.google.com/o/oauth2/auth',
                                                     :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
                                                     :client_id => ENV['client_id'],
                                                     :client_secret => ENV['client_secret'],
                                                     :refresh_token => ENV['refresh_token']
                                                 })
    else
      authorization = Signet::OAuth2::Client.new({
                                                     :authorization_uri => 'https://accounts.google.com/o/oauth2/auth',
                                                     :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
                                                     :client_id => ENV['client_id'],
                                                     :client_secret => ENV['client_secret'],
                                                     :refresh_token => ENV['refresh_token']
                                                 })
      begin
        authorization.fetch_access_token!
      rescue Exception => e  
        puts e.message  
        $dz.error('Redo authorization', 'Authorization failed. Please redo the authorization from the action\'s Edit screen.')
      end

      $dz.save_value('access_token', authorization.access_token)
      $dz.save_value('expires_at', (Time.now + authorization.expires_in).to_i)
    end

    authorization
  end

  def upload_file (file_path, folder_id)
    if File.directory?(file_path)
      $dz.error("Uploading folders not supported", "The Google Drive action does not currently support uploading of folders. Email support@aptonic.com if you need this feature.")
    end
    
    file_name = file_path.split(File::SEPARATOR).last
    $dz.begin("Uploading #{file_name} to Google Drive...")
    content_type = `file -Ib #{file_path}`.gsub(/\n/, "")

    file = Drive::File.new(title: file_name, :mime_type => content_type)
    parent = Drive::ParentReference.new(id: folder_id, is_root: true)
    file.parents = [parent]
    
    @drive.insert_file(file, :upload_source => file_path, :content_type => content_type) do |res, err|
      if err
        $dz.error("Upload Failed", err.message)
      end
    end
  end

  def get_folders
    result = @drive.list_files(q: "'root' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false")

    # using an array and a struct to guarantee order
    folders = Array.new
    result.items.each { |item|
      folders << Folder.new(item.title, item.id)
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

    file = Drive::File.new(title: folder_name, :mime_type => content_type)

    result = @drive.insert_file(file, :content_type => content_type) do |res, err|
      if err
        $dz.error("Failed to create folder", err.message)
      end
    end
    
    result.id
  end

end
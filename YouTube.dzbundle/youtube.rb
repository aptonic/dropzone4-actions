require 'bundler/setup'
require 'google/api_client'
require 'google/api_client/client_secrets'
require 'google/api_client/auth/installed_app'
require 'cgi'

class Youtube
  API_VERSION = 'v3'
  CACHED_API_FILE = "youtube-#{API_VERSION}.cache"
  CREDENTIAL_STORE_FILE = 'oauth2.json'
  Folder = Struct.new(:title, :folder_id)

  def configure_client
    $dz.begin('Connecting to YouTube...')

    unique_client_id = ENV['unique_client_id']
    if unique_client_id.nil? or unique_client_id.to_s.strip.length == 0
      unique_client_id = urlsafe_base64
      $dz.save_value('unique_client_id', unique_client_id)
    end

    temp_file_base_path = "#{$dz.temp_folder}/#{unique_client_id}"

    @client = Google::APIClient.new(:application_name => 'Dropzone 3 action for YouTube',
                                    :application_version => '1.0.0')
    @client.authorization = get_authorization

    @youtube = nil
    temp_cached_api_file = "#{temp_file_base_path}_#{CACHED_API_FILE}"
    if File.exists? temp_cached_api_file
      File.open(temp_cached_api_file) do |file|
        @youtube = Marshal.load(file)
      end
    else
      @youtube = @client.discovered_api('youtube', API_VERSION)
      File.open(temp_cached_api_file, 'w') do |file|
        Marshal.dump(@youtube, file)
      end
    end

  end

  def get_authorization
    if ENV['expires_at'].nil? or ENV['access_token'].nil?
      $dz.error('Redo authorization', 'The authorization data is not complete. Please redo the authorization from the action\'s Edit screen')
    end

    token_expiration_time_ms = ENV['expires_at'].to_i
    if token_expiration_time_ms > Time.now.to_i
      authorization = Signet::OAuth2::Client.new({
                                                     :authorization_uri => 'https://accounts.google.com/o/oauth2/auth',
                                                     :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
                                                     :client_id => ENV['client_id'],
                                                     :client_secret => ENV['client_secret'],
                                                     :access_token => ENV['access_token']
                                                 })
    else
      authorization = Signet::OAuth2::Client.new({
                                                     :authorization_uri => 'https://accounts.google.com/o/oauth2/auth',
                                                     :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
                                                     :client_id => ENV['client_id'],
                                                     :client_secret => ENV['client_secret'],
                                                     :refresh_token => ENV['refresh_token']
                                                 })
      authorization.fetch_access_token!

      $dz.save_value('access_token', authorization.access_token)
      $dz.save_value('expires_at', (Time.now + authorization.expires_in).to_i)
    end

    authorization
  end

  def upload_video (file_path, privacy_status)
    file_name = file_path.split(File::SEPARATOR).last
    $dz.begin("Uploading #{file_name} to YouTube...")
    content_type = `file -Ib #{file_path}`.gsub(/\n/, "")


    file = @youtube.videos.insert.request_schema.new({
                                                         :status => {
                                                             :privacyStatus => privacy_status
                                                         }
                                                     })

    media = Google::APIClient::UploadIO.new(file_path, content_type)
    result = @client.execute(
        :api_method => @youtube.videos.insert,
        :body_object => file,
        :media => media,
        :parameters => {
            :uploadType => 'multipart',
            :part =>  ['status']
        })

    unless result.success?
      $dz.error(result.error_message)
    end

    system("open 'https://www.youtube.com/edit?o=U&video_id=#{result.data.id}'")
  end

  def read_privacy_status
    output = $dz.cocoa_dialog("standard-dropdown --button1 \"OK\" --button2 \"Cancel\" --title \"Privacy status\" --text \"Would you like the video to be public, private or unlisted?\" --items \"public\" \"private\" \"unlisted\" ")
    button, privacy_index = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
    end

    case privacy_index
      when '1'
        privacy_status = 'private'
      when '2'
        privacy_status = 'unlisted'
      else
        privacy_status = 'public'
    end

    privacy_status
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
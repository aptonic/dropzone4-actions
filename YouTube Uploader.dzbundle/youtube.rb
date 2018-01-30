require 'google/apis/youtube_v3'

class Youtube
  Youtube = Google::Apis::YoutubeV3
  
  def configure_client
    $dz.begin('Connecting to YouTube...')

    @youtube = Youtube::YouTubeService.new
    @youtube.authorization = get_authorization
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

  def upload_video (file_path, privacy_status)
    file_name = file_path.split(File::SEPARATOR).last
    $dz.begin("Uploading #{file_name} to YouTube...")
    content_type = `file -Ib \"#{file_path}\"`.gsub(/\n/, "")

    metadata  = {
     snippet: {
       title: File.basename(file_name, ".*")
     },
     status: {
       privacy_status: privacy_status
     }
    }
    result = @youtube.insert_video('snippet,status', metadata, upload_source: file_path)

    system("open 'https://www.youtube.com/edit?o=U&video_id=#{result.id}'")
  end

  def read_privacy_status
    output = $dz.cocoa_dialog("standard-dropdown --button1 \"OK\" --button2 \"Cancel\" --title \"Privacy status\" --text \"Would you like the dropped video(s) to be public, private or unlisted?\" --items \"public\" \"private\" \"unlisted\" ")
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
end
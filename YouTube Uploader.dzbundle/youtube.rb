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
    last_privacy = if ENV['privacy'].nil? then 'Unlisted' else ENV['privacy'] end
    pconfig = "
        *.title = Youtube Uploader
        privacy.type = popup
        privacy.label = Would you like the dropped video(s) to be public, private or unlisted?
        privacy.option = Public
        privacy.option = Private
        privacy.option = Unlisted
        privacy.default = #{last_privacy}
        bc.type = cancelbutton
        bc.default = Cancel
        db.type = defaultbutton
        db.label = Upload
    "

    result = $dz.pashua(pconfig)

    if result['bc'] == '1'
      $dz.fail('Upload cancelled')
    end

    privacy_status = result['privacy']
    $dz.save_value('privacy', privacy_status)

    privacy_status.downcase
  end
end

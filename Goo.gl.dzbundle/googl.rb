require 'cgi'
require 'rexml/document'
require 'uri'
require 'net/http'
require 'net/https'
require 'json'
require 'lib/google/api_client'
require 'lib/google/api_client/auth/file_storage'
require 'lib/google/api_client/auth/installed_app'
require 'securerandom'

class Googl
  API_VERSION = 'v1'
  CACHED_API_FILE = "urlshortener-#{API_VERSION}.cache"
  CREDENTIAL_STORE_FILE = 'oauth2.json'

  def configure_client
    unique_client_id = ENV['unique_client_id']
    if unique_client_id.nil? or unique_client_id.to_s.strip.length == 0
      unique_client_id = urlsafe_base64
      $dz.save_value('unique_client_id', unique_client_id)
    end

    temp_file_base_path = "#{$dz.temp_folder}/#{unique_client_id}"

    @client = Google::APIClient.new(:application_name => 'Dropzone 3 action for Goo.gl',
                                    :application_version => '1.0.0')

    @client.authorization = get_authorization

    @urlshortener = nil
    temp_cached_api_file = "#{temp_file_base_path}_#{CACHED_API_FILE}"
    if File.exists? temp_cached_api_file
      File.open(temp_cached_api_file) do |file|
        @urlshortener = Marshal.load(file)
      end
    else
      @urlshortener = @client.discovered_api('urlshortener', API_VERSION)
      File.open(temp_cached_api_file, 'w') do |file|
        Marshal.dump(@urlshortener, file)
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

  def process(item)
    $dz.determinate(false)
    $dz.begin('Getting Goo.gl URL')

    if item =~ /http/
      if item =~ /http:\/\/goo.gl\//
        expand_url(item)
      else
        shorten_url(item)
      end
    else
      $dz.finish('Invalid URL')
      $dz.url(false)
    end
  end

  def shorten_url(url_to_shorten)
    url_details = @urlshortener.url.insert.request_schema.new( { :longUrl => url_to_shorten } )
    result = @client.execute(
        :api_method => @urlshortener.url.insert,
        :body_object => url_details
    )

    unless result.success?
      $dz.error('Goo.gl Failed to shorten URL', "#{result.status} #{result.error_message}")
    end

    short_url = result.data.id

    if short_url.nil? || short_url.to_s.strip.length == 0
      $dz.finish('Goo.gl failed to shortcut your URL!')
      $dz.url(false)
    else
      $dz.finish('Goo.gl Shortened URL is now on clipboard')
      $dz.url(short_url)
    end
  end

  def expand_url(url_to_expand)
    result = @client.execute(
        :api_method => @urlshortener.url.get,
        :parameters => {
            :shortUrl => url_to_expand
        })

    unless result.success?
      $dz.error('Goo.gl Failed to Expand URL', "#{result.status} #{result.error_message}")
    end

    expanded_url = result.data['longUrl']

    if expanded_url.nil? || expanded_url.to_s.strip.length == 0
      # Failed Expand URL
      $dz.alert('Goo.gl Failed to Expand URL')
      $dz.finish('Expand URL Failed')
    else
      # Expand URL
      $dz.url(expanded_url)
      $dz.finish("Goo.gl expanded URL for #{item} is now on clipboard")
    end
  end

  def read_clipboard
    IO.popen('pbpaste') { |clipboard| clipboard.read }
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
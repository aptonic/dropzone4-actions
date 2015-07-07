require 'google/api_client'
require 'google/api_client/client_secrets'
require 'google/api_client/auth/installed_app'
require 'securerandom'
require 'cgi'
require 'rexml/document'
require 'uri'
require 'net/http'
require 'net/https'
require 'json'

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
    authorization = nil

    unless ENV['expires_at'].nil? or ENV['access_token'].nil?
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
    else
      @client.key = ENV['api_key'] unless ENV['api_key'].nil?
    end

    authorization
  end

  def process(item)
    if item =~ /http:\/\/goo\.gl\/*$/ or item =~ /https:\/\/goo\.gl\/*$/
      $dz.error('Invalid URL', 'You cannot expand or shorten the Google url shortener base domain!')
    end

    begin
      url = URI.parse(item)
      url = URI.parse("http://" + item) unless url.scheme
    rescue URI::InvalidURIError
      $dz.fail("Invalid URL")
    end

    url_as_string = url.to_s

    if url_as_string =~ /https?:\/\/goo\.gl\//
      expand_url(url_as_string)
    else
      shorten_url(url_as_string)
    end
  end

  def shorten_url(url_to_shorten)
    url_details = @urlshortener.url.insert.request_schema.new( { :longUrl => url_to_shorten } )
    result = @client.execute(
        :api_method => @urlshortener.url.insert,
        :body_object => url_details
    )

    unless result.success?
      $dz.error('Failed to shorten URL', "#{result.status} #{result.error_message}")
    end

    short_url = result.data.id

    if short_url.nil? || short_url.to_s.strip.length == 0
      $dz.fail('Error shortening URL')
    else
      $dz.finish("URL is now on clipboard")
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
      $dz.error('Failed to Expand URL', "#{result.status} #{result.error_message}")
    end

    expanded_url = result.data['longUrl']

    if expanded_url.nil? || expanded_url.to_s.strip.length == 0
      # Failed Expand URL
      $dz.fail('Error expanding URL')
    else
      # Expand URL
      $dz.finish("Expanded URL is now on clipboard")
      $dz.url(expanded_url)
    end
  end

  def read_clipboard
    IO.popen('pbpaste') { |clipboard| clipboard.read }
  end

  def urlsafe_base64(n=nil, padding=false)
    s = [SecureRandom.random_bytes(n)].pack('m*')
    s.delete!("\n")
    s.tr!('+/', '-_')
    s.delete!('=') unless padding
    s
  end
end
# Dropzone Action Info
# Name: Bitly
# Description: A dropped URL will be converted to a Bit.ly URL. Password is your API key which can be found at http://bit.ly/a/your_api_key
# Handles: Text
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: Login
# LoginTitle: Bitly Login Details
# Version: 1.6
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1013

require 'uri'
require 'rest-client'
require 'multi_json'
 
def dragged
  shorten($items[0])
end

def shorten(item)
  $dz.determinate(false)
  $dz.begin("Getting Bitly URL...")
  
  begin
    enc_url = URI.encode(item)
    url = URI.parse(enc_url)
    url = URI.parse("http://" + enc_url) unless url.scheme
  rescue URI::InvalidURIError
    $dz.fail("Invalid URL")
  end
  
  begin
    response = RestClient.get 'https://api-ssl.bitly.com/v3/shorten', {:params => {:login => ENV['username'], :apiKey => ENV['password'], :longUrl => URI.unescape(url.to_s)}}
  rescue
    puts $!
    $dz.fail("Failed to connect to Bitly")
  end
  
  begin
    result = MultiJson.load(response.body)
  rescue
    puts $!
    show_response_invalid_error(response)
  end
  
  if result['status_txt'] == 'OK'
    $dz.finish("URL is now on clipboard")
    $dz.url(result['data']['url'])
  elsif result['status_txt'] == "INVALID_LOGIN"
    $dz.fail("Invalid Username or API key")
  elsif result['status_txt'] == "ALREADY_A_BITLY_LINK"
    $dz.fail("Already a Bitly link")
  elsif result['status_txt'] == "INVALID_URI"
    $dz.fail("Invalid URL")
  else
    show_response_invalid_error(response)
  end
end 

def show_response_invalid_error(response)
  puts response.body if response
  $dz.fail("Error shortening URL.\nSee Dropzone debug console for details.")
end

def readClipboard
  IO.popen('pbpaste') {|clipboard| clipboard.read}
end
 
def clicked
  data = readClipboard()
  shorten(data)
end

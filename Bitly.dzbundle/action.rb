# Dropzone Action Info
# Name: Bitly
# Description: A dropped URL will be converted to a Bit.ly URL. Password is your API key which can be found at http://bit.ly/a/your_api_key
# Handles: Text
# Creator: Sergej Müller
# URL: http://ebiene.de
# OptionsNIB: Login
# LoginTitle: Bitly Login Details
# Version: 1.0
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# UniqueID: 1013

require 'cgi'
require 'rexml/document'
require 'net/https'
require 'uri'
 
def dragged
  shorten($items[0])
end

def shorten(item)
  $dz.determinate(false)
  $dz.begin("Getting Bitly URL")
  
  if item =~ /http/
    username = ENV['username']
    apikey = ENV['password']
    url = CGI::escape(item)

    version = "2.0.1"
    uri = URI.parse("http://api.bit.ly/shorten?version=#{version}&format=xml&longUrl=#{url}&login=#{username}&apiKey=#{apikey}")
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

    doc = REXML::Document.new(response.body)
    doc.elements.each("bitly/errorMessage") do |a|
      if a.text == "INVALID_LOGIN"
        $dz.fail("Invalid user or API key")
      elsif a.text == "ALREADY_A_BITLY_LINK"
        $dz.fail("Already a bit.ly link")
      else
         doc.elements.each("bitly/results/nodeKeyVal/shortUrl") do |b|
           if b.text.empty?
             $dz.fail("Empty URL is returned")
           else
             $dz.finish("URL is now on clipboard")
             $dz.url(b.text)
           end
         end
       end
     end
  else
    $dz.fail("Invalid URL")
  end
end

def readClipboard
	IO.popen('pbpaste') {|clipboard| clipboard.read}
end
 
def clicked
  data = readClipboard()
  shorten(data)
end

# Dropzone Action Info
# Name: TwitPic
# Description: Share photos via the TwitPic service. Copies the TwitPic URL to the clipboard. Does not tweet automatically.
# Handles: Files
# Events: Clicked, Dragged, Authorize, Get_Token
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: TwitPicAuth
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0

require "rexml/document"
require "oauth"
require "stash"

$contact_info = "\n\nIf you continue to have problems, email support@aptonic.com"

def authorize
  system("/bin/rm -f #{$dz.temp_folder}/request_token.stash")
  consumer = OAuth::Consumer.new(ENV['consumer_key'], ENV['consumer_secret'],
    { :site => "https://api.twitter.com",
      :scheme => :header
    })

  begin
    request_token = consumer.get_request_token()
  rescue SocketError, NoMethodError
    $dz.error("Connection Error", "Failed to connect to api.twitter.com\nCheck your internet connection and try again.")
  rescue => e
    $dz.error("Authorization Error", "Could not get a request token.\nError: #{e.message}#{$contact_info}")
  end
  ObjectStash.store request_token, "#{$dz.temp_folder}/request_token.stash"
  $dz.send_output("OAuth_URL: #{request_token.authorize_url}")
end

def get_token
  # Use pin to return ouath_token & oauth_secret for saving in DB by Dropzone
  request_token = ObjectStash.load "#{$dz.temp_folder}/request_token.stash"
  begin
    access_token = request_token.get_access_token :oauth_verifier => ENV['pincode']
  rescue => e
    $dz.error("Authorization Error", "Could not validate the pin code.\nError: #{e.message}#{$contact_info}")
  end
  outh_token = access_token.token
  oauth_secret = access_token.secret
  $dz.send_output("OAuth_Info: #{outh_token},#{oauth_secret}")
end

def dragged
  $dz.determinate(true)
  
  file_path = $items[0]
  filename = File.basename(file_path)
  should_tweet = false
  tweet_text = ""
  
  allowed_exts = ["jpg", "jpeg", "gif", "tif", "tiff", "png", "bmp"]
  ext = File.extname(file_path).downcase[1..-1]
  
  if not allowed_exts.include?(ext)
    $dz.finish("Not an Image")
    $dz.url(false)
    Process.exit
  end
  
  $dz.begin("Uploading #{filename}...")

  last_output = 0
  is_receiving_xml = false
  xml_output = ""
 
  file_path = file_path.gsub('"', '\"')
  oauth_token,oauth_secret = ENV['access_token'].split(",")
  
  IO.popen("curl -# -F \"consumer_token=#{ENV['consumer_key']}\" -F \"consumer_secret=#{ENV['consumer_secret']}\" -F \"oauth_token=#{oauth_token}\" -F \"oauth_secret=#{oauth_secret}\" -F \"key=#{ENV['api_key']}\" -F \"media=@#{file_path}\" http://api.twitpic.com/1/upload.xml 2>&1 | tr -u \"\r\" \"\n\"") do |f|
    while line = f.gets do
      if line =~ /%/ and not is_receiving_xml
        line_split = line.split(" ")
        file_percent_raw = line_split[1]
        if file_percent_raw != nil
          file_percent = file_percent_raw.to_i
          if last_output != file_percent
            $dz.percent(file_percent) 
            $dz.determinate(false) if file_percent == 100
          end
          last_output = file_percent
        end
      else
        if line =~ /xml/ or is_receiving_xml
          is_receiving_xml = true
          xml_output += line
        else
          handle_errors(line)
        end
      end
    end
  end

  begin
    url = ""
    doc = REXML::Document.new(xml_output)
    root = doc.root
    
    if doc.elements["image/url"] != nil
      url = doc.elements["image/url"].text
    else
      $dz.error("TwitPic Upload Error", "Received an invalid response from the TwitPic API. Please try your upload again.#{$contact_info}")
    end

    $dz.finish("URL is now on clipboard")
    $dz.url(url)
  rescue
    $dz.finish("Upload Failed")
    $dz.url(false)
  end
end

def handle_errors(line)
  if line[0..4] == "curl:"
    if line[6..-1] =~ /Could not resolve/
      $dz.error("TwitPic Upload Error", "Failed to connect to api.twitpic.com\nCheck your internet connection and try again.")
    else
      $dz.error("TwitPic Upload Error", line[6..-1])
    end
  end
end

def clicked
  system("open http://twitpic.com/")
end

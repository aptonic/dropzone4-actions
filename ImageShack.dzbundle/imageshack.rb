require 'json'
require 'uri'
require 'net/https'

class ImageShack
  attr_accessor :error_message
  
  def get_auth_token(username, password)
    uri = URI.parse("https://api.imageshack.com/v2/user/login")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_PEER
    request = Net::HTTP::Post.new(uri.request_uri)
    request["Content-Type"] = "application/x-www-form-urlencoded"

    request.set_form_data({
    	"user" => username,
    	"password" => password,
    })
    
    begin
      response = http.request(request)
      json = JSON.parse(response.body)
    rescue
      @error_message = $!
      return
    end
    
    if json["result"] and json["result"]["auth_token"]
      return json["result"]["auth_token"]
    else
      if json["error"] and json["error"]["error_message"]
        @error_message = json["error"]["error_message"]
      else
        puts response.body
        @error_message = "Invalid JSON received"
      end
      return nil
    end
  end
  
  def get_url(json_output)
    begin
      extracted_json = /\{".*\}/.match(json_output)[0]
      json = JSON.parse(extracted_json)
    rescue
      puts json_output
      @error_message = $!
      return
    end
      
    if json["result"] and json["result"]["images"].length > 0
      return json["result"]["images"][0]["direct_link"]
    else
      if json["error"] and json["error"]["error_message"]
        @error_message = json["error"]["error_message"]
      else
        @error_message = "Invalid JSON received"
      end
      puts json_output
      return nil
    end
  end
end
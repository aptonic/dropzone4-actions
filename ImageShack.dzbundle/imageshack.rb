require 'post_request'
require 'json'
require 'uri'
require 'net/https'

class ImageShack
  attr_accessor :error_message
  
  def get_auth_token(username, password)
    form_data = {
    	:user => username,
    	:password => password
    }

    post_request = PostRequest.new("https://api.imageshack.com/v2/user/login", form_data)
    
    begin
      response = post_request.post
      json = JSON.parse(response)
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
  
  def get_url(json)
    if json["result"] and json["result"]["images"].length > 0
      return json["result"]["images"][0]["direct_link"]
    else
      if json["error"] and json["error"]["error_message"]
        @error_message = json["error"]["error_message"]
      else
        @error_message = "Invalid JSON received"
      end
      return nil
    end
  end
  
  def create_album(album_name, auth_token)
    form_data = {
      :api_key => ENV['api_key'],
      :auth_token => auth_token,
    	:title => album_name
    }

    post_request = PostRequest.new("https://api.imageshack.com/v2/albums", form_data)

    album_creation_success = false

    begin
      response = post_request.post
      json = JSON.parse(response)
      if json["success"] and json["result"] and json["result"]["id"]
        album_creation_success = true
      else
        album_creation_success = false
      end
    rescue
      album_creation_success = false
      error_message = $!
    end
    
    if (album_creation_success)
      return json
    else
      puts response
      if json["error"] and json["error"]["error_message"]
        error_output = json["error"]["error_message"]
      else
        error_output = (error_message ? "Error:: #{error_message}\n\nResponse: #{response}" : "Response not valid:: #{response}")
      end
      $dz.error("Album creation failed", "The album could not be created.\n\n#{error_output}")
    end
    
  end
end
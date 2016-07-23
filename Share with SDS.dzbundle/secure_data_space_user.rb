
require 'rest_client'
require 'json'

class SecureDataSpaceUser
  
  attr_reader :auth_token, :id, :login, :first_name, :last_name, :title, :gender, :customer_id, :customer_name, :raw
  
  def initialize(sds, auth_token, path="/api/v3")
    @auth_token = auth_token
    @sds = sds
    @path = path
    
    begin
      api = "/user/account"
      response = RestClient.get "#{sds.host}#{@path}#{api}", {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}

      @raw =JSON.parse(response)
      @id = @raw["id"]
      @login = @raw["login"]
      @first_name = @raw["firstName"]
      @last_name = @raw["lastName"]
      @title = @raw["title"]
      @gender = @raw["gender"]
      @customer_id = @raw["customer"]["id"]
      @customer_name = @raw["customer"]["name"]
      
    rescue
      puts $!
    end
    
  end
  
  
  def to_s
    @login
  end
  
  
  def customer
    @raw["customer"]
  end
  
  
  def logout
    @sds.logout
  end
  
  
end

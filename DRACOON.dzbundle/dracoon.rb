require 'rest-client'
require 'multi_json'

class Dracoon
  attr_reader :host, :auth_token, :user
  PATH = "/api/v4"
  VALID_RESOLUTION_STRATEGIES = ['autorename', 'fail', 'overwrite']
  MIN_VERSION = "4.23.0"
  USER_AGENT = "DRACOON for Dropzone v2.0"


  def initialize(host)
    @host = host.strip

    # Protocol required
    if !@host.start_with?("https://") && !@host.start_with?("http://")
      fail("Please enter Server with https:// or http://")
    end

    # Remove trailing /
    if @host.end_with?("/")
      @host = @host.slice(0,@host.size-1)
    end

    # Check connectivity
    begin
      api = "/public/software/version"
      response = RestClient.get "#{@host}#{PATH}#{api}", {:accept => :json, :user_agent => USER_AGENT}
      api_version = MultiJson.load(response)["restApiVersion"]
      @path = PATH
    rescue => e
      raise StandardError.new $!
    end

    version = api_version.split('.').map{|v| v.to_i}
    min_version = MIN_VERSION.split('.').map{|v| v.to_i}

    unless (version <=> min_version) == 1
      fail("Incompatible API version. Actual: #{api_version}; required: #{MIN_VERSION}")
    end
  end
  

  def authorize
    # no authorization available
    if ENV["authorization_token"] == nil
      code = start_authorization
  
      authorization_token, refresh_token = get_tokens_by_code(code)
      $dz.save_value('authorization_token', authorization_token)
      $dz.save_value('refresh_token', refresh_token)
      ENV["authorization_token"] = authorization_token
      return

    else
      begin
        authorization_token, refresh_token = get_tokens_by_refresh_token
        $dz.save_value('authorization_token', authorization_token)
        $dz.save_value('refresh_token', refresh_token)
        ENV["authorization_token"] = authorization_token
        return
      rescue StandardError => e
        #expired refresh token or other issue
        code = start_authorization
  
        authorization_token, refresh_token = get_tokens_by_code(code)
        $dz.save_value('authorization_token', authorization_token)
        $dz.save_value('refresh_token', refresh_token)  
        ENV["authorization_token"] = authorization_token
        return   
      end
    end
  end


  def start_authorization
    auth_url = "#{host}/oauth/authorize?branding=full&response_type=code&client_id=Phc9SxLh17WY8cxzilAJWh0hICXZAqh7&redirect_uri=#{@host}/oauth/callback&scope=all"
    %x{open "#{auth_url}"}
    dialog = "
    *.title = DRACOON Authorization
    p.type = textfield
    p.label = Paste Authorization Code
    "
    code = $dz.pashua(dialog)["p"]
    return code
  end


  def get_tokens_by_code(code)
    begin
      api = "#{@host}/oauth/token"
      response = RestClient.post api, {"code" => code, "grant_type" => "authorization_code", "redirect_uri" => "#{@host}/oauth/callback", "client_id" => "Phc9SxLh17WY8cxzilAJWh0hICXZAqh7", "client_secret" => "OEqVy6HCKCLmnHlzsEvrtCTCp4BOfvLj"}, {:accept => :json, :content_type => "application/x-www-form-urlencoded", :user_agent => USER_AGENT}
      data = MultiJson.load(response)
      return data["access_token"], data["refresh_token"]

    rescue StandardError => e
      puts $!
      puts e.response
      return nil, nil
    end
  end
  
  
  def get_tokens_by_refresh_token
    api = "#{@host}/oauth/token"
    response = RestClient.post api, {"grant_type" => "refresh_token", "refresh_token" => "#{ENV["refresh_token"]}", "client_id" => "Phc9SxLh17WY8cxzilAJWh0hICXZAqh7", "client_secret" => "OEqVy6HCKCLmnHlzsEvrtCTCp4BOfvLj"}, {:accept => :json, :content_type => "application/x-www-form-urlencoded", :user_agent => USER_AGENT}
    data = MultiJson.load(response)
    return data["access_token"], data["refresh_token"]
  end
  
  
  def get_profile
    begin
      api = "#{@host}#{@path}/user/account"
      
      response = RestClient.get api, {:accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      return MultiJson.load(response)

    rescue StandardError => e
      retries = 0
      
      if e.response.code == 401
        authorize
        retry if (retries += 1) < 2
      elseif e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3 
      else
        puts $!
        puts e.response
        return nil
      end
    end  
  end
  
  
  def check_password_compliance(password)
    
    # get policy
    begin
      api = "#{@host}#{@path}/config/info/policies/passwords"
    
      response = RestClient.get api, {:accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      policies = MultiJson.load(response)["sharesPasswordPolicies"]
      
    rescue StandardError => e
      retries = 0
      
      if e.response.code == 401
        authorize
        retry if (retries +=1) <2
      else
        puts $!
        puts e.response
      end
    end
    
    return false if password.length < policies["minLength"]
    return false if (policies["characterRules"]["mustContainCharacters"].include? 'lowercase') && (/[a-z]/.match(password) == nil)
    return false if (policies["characterRules"]["mustContainCharacters"].include? 'numeric') && (/[0-9]/.match(password) == nil)
    return false if (policies["characterRules"]["mustContainCharacters"].include? 'uppercase') && (/[A-Z]/.match(password) == nil)
    return false if (policies["characterRules"]["mustContainCharacters"].include? 'special') && (/[\W]/.match(password) == nil)
    
    return true
  end
  
  
  def get_homeroom_path
    
    profile = get_profile
    homeroom_id = profile["homeRoomId"]
    
    return get_path_by_node_id homeroom_id 
  end
  
  
  def get_path_by_node_id(id)
    begin
      api = "#{@host}#{@path}/nodes/#{id}"
    
      response = RestClient.get api, {:accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      node = MultiJson.load(response)
      return "#{node["parentPath"]}#{node["name"]}"
      
    rescue StandardError => e
      puts $!
      puts e.response
    end
    
    return nil
  end
  
  
  def get_node_by_name(name, parent_id = 0)
    begin
      api = "#{@host}#{@path}/nodes?parent_id=#{parent_id}&filter=name%3Aeq%3A#{ERB::Util.url_encode(name)}"
      
      response = RestClient.get api, {:accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      data = MultiJson.load(response)
      
      if data["range"]["total"] != 1
        return nil
      else
        return data["items"][0]
      end
      
    rescue StandardError => e
      retries = 0
      if e.response.code == 401
        authorize
        retry if (retries += 1) < 2
      elseif e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      else
        raise e
      end
    end
  end
  
  
  def create_room(name, parent_id = nil)
    
    user_id = get_user_id
    admin_ids = [user_id]
    if parent_id == 0
      parent_id = nil
    end
    
    begin
      api = "#{@host}#{@path}/nodes/rooms"
      response = RestClient.post api, MultiJson.dump({'name' => name, 'parentId' => parent_id, 'adminIds' => admin_ids}), {:content_type => :json, :accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      return MultiJson.load(response)
    rescue StandardError => e
      retries = 0
      puts $!
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end
  end
  
  
  def create_folder(name, parent_id = 0)
    
    begin
      api = "#{@host}#{@path}/nodes/folders"
      
      response = RestClient.post api, MultiJson.dump({'name' => name, 'parentId' => parent_id}), {:content_type => :json, :accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      return MultiJson.load(response)
    rescue StandardError => e
      retries = 0
      
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end
  end
  
  
  def get_user_id
    return get_profile["id"]
  end
  
  
  def upload_file(file, parent_id, expiryDate = nil)
    
    if !File.file? file
      fail("File does not exist or is not accessible!")
    end
    file_name = File.basename file
    file_size = File.new(file).size
    
    # Create upload channel
    begin
      api = "#{@host}#{@path}/nodes/files/uploads"
      if expiryDate == nil
        expiration = nil
      else
        expiration = {'expireAt' => expiryDate.to_s, 'enableExpiration' => true}
      end
      response = RestClient.post api, MultiJson.dump({'parentId' => parent_id,'name' => file_name, 'size' => file_size, 'expiration' => expiration}), {:content_type => :json, :accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}

      @upload_url = MultiJson.load(response)["uploadUrl"]
    rescue StandardError => e
      retries = 0
      
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end

    # Upload file
    begin
      response = RestClient.post @upload_url, {:multipart => true, :file => File.new(file)}, {:accept => :json, :user_agent => USER_AGENT}
    rescue StandardError => e
      retries = 0
      
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end

    # Finish upload
    begin
      response = RestClient.put @upload_url, MultiJson.dump({'resolutionStrategy' => 'autorename'}), {:content_type => :json, :accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      file_info = MultiJson.load(response)
    rescue StandardError => e
      retries = 0
      
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end

    return file_info   
  end
  
  
  def create_download_share(node_id, share_password = nil, expiryDate = nil)
    if !node_id.is_a? Integer
      fail("Node ID must be an Integer.")
    end

    begin
      api = "#{@host}#{@path}/shares/downloads"
      if expiryDate == nil
        expiration = nil
      else
        expiration = {'expireAt' => expiryDate.to_s, 'enableExpiration' => true}
      end
      response = RestClient.post api, MultiJson.dump({'nodeId' => node_id, 'password' => share_password, 'expiration' => expiration}), {:content_type => :json, :accept => :json, :Authorization => "Bearer #{ENV["authorization_token"]}", :user_agent => USER_AGENT}
      share = MultiJson.load(response)

    rescue StandardError => e
      retries = 0
      
      puts $!
      if e.response.code == 500 || e.response.code == 503 || e.response.code == 504
        retry if (retries += 1) < 3
      end
    end

    link = "#{@host}/#/public/shares-downloads/#{share["accessKey"]}"
    share["link"] = link
    return share
  end
  
end
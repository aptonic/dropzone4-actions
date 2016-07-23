
require 'rest_client'
require 'json'
require 'Date'
require 'digest'
require 'securerandom'
require 'uri'
require './secure_data_space_user'


class SecureDataSpace
  attr_reader :host, :auth_token, :user
  PATH = "/api/v3"
  ADDITIONAL_PATH = "/api/v4"
  VALID_RESOLUTION_STRATEGIES = ['autorename', 'fail', 'overwrite']
  VALID_LANGUAGES = ['de', 'en']


  def initialize (host)
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
      response = RestClient.get "#{@host}#{PATH}#{api}", {:accept => :json}
      api_version = JSON.parse(response)["restApiVersion"]
      @path = PATH
    rescue
      begin
        response = RestClient.get "#{@host}/#{ADDITIONAL_PATH}#{api}", {:accept => :json}
        api_version = JSON.parse(response)["restApiVersion"]
        @path = ADDITIONAL_PATH
      rescue
        puts $!
      end
    end
    
    if !api_version.start_with?("3.") && !api_version.start_with?("4.")
      puts "FAIL. No supported API version at #{@path}: #{api_version}"
    end
    
  end
  
  
  def to_s
    @host
  end


  def login(username, password, create_user_object = true, language = nil)
    if language != nil && !(VALID_LANGUAGES.include? language)
      fail("Invalid resolution language.")
    end
    
    begin
      api = "/auth/login"
      response = RestClient.post "#{@host}#{@path}#{api}", { 'login' => username, 'password' => password, 'language' => language }.to_json, {:content_type => :json, :accept => :json}
      @auth_token = JSON.parse(response)["token"]
    rescue
      puts $!
      return nil
    end
    
    if create_user_object
      self.set_user_object
    end
    
    @auth_token
  end

  
  def logout
    self.login_required
    
    begin
      api = "/user/logout"
      response = RestClient.post "#{@host}#{@path}#{api}", {}, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
    rescue
      puts $!
      fail("Could not log out.")
    end
    true
  end


  def set_user_object
    self.login_required
    
    if @user
      @user
    else
      @user = SecureDataSpaceUser.new self, @auth_token, @path
    end
  end

  
  def nodes(parent_id = 0, depth_level = 0, filter = nil, sort = nil, offset = nil, limit = nil)
    self.login_required
    
    params = "?parent_id=#{parent_id}&depth_level=#{depth_level}"
    if filter != nil
      params = params + "&filter=#{filter}"
    end
    if sort != nil
      params = params + "&sort=#{sort}"
    end
    if offset != nil
      params = params + "&offset=#{offset}"
    end
    if limit != nil
      params = params + "&limit=#{limit}"
    end
    
    begin
      api = "/nodes"
      response = RestClient.get "#{@host}#{@path}#{api}#{params}", {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      nodes = JSON.parse(response)
    rescue
      puts $!
      fail("Could not retrieve nodes.")
    end
    
    nodes
  end
  
  
  def get_nodes_by_name(name, parent_id = 0, depth_level = 0)
    self.login_required

    nodes(parent_id, depth_level, filter = "name:cn:#{URI.escape(name)}")
  end
  
  
  def create_room(name, parent_id = nil, admin_ids = nil, quota = nil, has_recycle_bin = nil, recycle_bin_retention_period = nil)
    self.login_required
    
    if admin_ids == nil
      admin_ids = [@user.id]
    end
    
    begin
      api = "/nodes/rooms"
      response = RestClient.post "#{@host}#{@path}#{api}", {'name' => name, 'parentId' => parent_id, 'adminIds' => admin_ids, 'quota' => quota, 'hasRecycleBin' => has_recycle_bin, 'recycleBinRetentionPeriod' => recycle_bin_retention_period}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      node = JSON.parse(response)
    rescue
      puts $!
      fail("Could not create room.")
    end
    
    node
  end


  def create_folder(name, parent_id)
    self.login_required
        
    begin
      api = "/nodes/folders"
      response = RestClient.post "#{@host}#{@path}#{api}", {'name' => name, 'parentId' => parent_id}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      node = JSON.parse(response)
    rescue
      puts $!
      fail("Could not create folder.")
    end
    node
  end


  def upload_file(file, parent_id, expire_at = nil, resolution_strategy = "autorename", classification = 1, notes = nil)
    self.login_required

    if !File.file? file
      fail("File does not exist or is not accessible!")
    end
    file_name = File.basename file
    file_size = File.new(file).size

    if !VALID_RESOLUTION_STRATEGIES.include? resolution_strategy
      fail("Invalid resolution strategy.")
    end
    
    # Create upload channel
    begin
      api = "/nodes/files/uploads"
      if @path == "api/v3"
        response = RestClient.post "#{@host}#{@path}#{api}", {'parentId' => parent_id,'name' => file_name, 'size' => file_size, 'classification' => classification, 'expireAt' => expire_at, 'notes' => notes}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      else
        if expire_at == nil
          expiration = nil
        else
          expiration = {'expireAt' => expire_at.to_s, 'enableExpiration' => true}
        end
        response = RestClient.post "#{@host}#{@path}#{api}", {'parentId' => parent_id,'name' => file_name, 'size' => file_size, 'classification' => classification, 'expiration' => expiration, 'notes' => notes}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      end
      @upload_id = JSON.parse(response)["uploadId"]
    rescue
      puts $!
      fail("Could not establish Upload Channel.")
    end

    # Upload file
    begin
      api = "/nodes/files/uploads"
      response = RestClient.post "#{@host}#{@path}#{api}/#{@upload_id}", {:multipart => true, :file => File.new(file)}, {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}
    rescue
      puts $!
      fail("Could not transfer file.")
    end

    # Finish upload
    begin
      api = "/nodes/files/uploads"
      response = RestClient.put "#{@host}#{@path}#{api}/#{@upload_id}",{'resolutionStrategy' => resolution_strategy}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      file_info = JSON.parse(response)
    rescue
      puts $!
      fail("Could not finish upload.")
    end
    
    file_info
  end


  def create_download_share(node_id, name = nil, password = nil, notify_creator = false, expire_at = nil, max_downloads = nil, show_creator_name = nil, show_creator_user_name = nil, send_mail = false, mail_recipients = nil, mail_subject = nil, mail_body = nil)
    self.login_required
    
    if !node_id.is_a? Integer
      fail("Node ID must be an Integer.")
    end
    
    if name == nil
      name = SecureRandom.uuid
    end
    
    begin
      api = "/shares/downloads"
      if @path == "api/v3"
        response = RestClient.post "#{@host}#{@path}#{api}", {'nodeId' => node_id, 'name' => name, 'password' => password, 'notifyCreator' => notify_creator, 'expireAt' => expire_at, 'maxDownloads' => max_downloads, 'showCreatorName' => show_creator_name, 'showCreatorUsername' => show_creator_user_name, 'sendMail' => send_mail, 'mailRecipients' => mail_recipients, 'mailSubject' => mail_subject, 'mailBody' => mail_body}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token} 
      else
        if expire_at == nil
          expiration = nil
        else
          expiration = {'expireAt' => expire_at.to_s, 'enableExpiration' => true}
        end
        response = RestClient.post "#{@host}#{@path}#{api}", {'nodeId' => node_id, 'name' => name, 'password' => password, 'notifyCreator' => notify_creator, 'expiration' => expiration, 'maxDownloads' => max_downloads, 'showCreatorName' => show_creator_name, 'showCreatorUsername' => show_creator_user_name, 'sendMail' => send_mail, 'mailRecipients' => mail_recipients, 'mailSubject' => mail_subject, 'mailBody' => mail_body}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token} 
      end

      share = JSON.parse(response)
    rescue
      puts $!
      fail("Could not create Download Share")
    end
    
    link = "#{@host}/#/public/shares-downloads/#{share["accessKey"]}"
    share["link"] = link
    share
  end


  def download_shares
    self.login_required
    
    begin
      api = "/shares/downloads"
      response = RestClient.get "#{@host}#{@path}#{api}", {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      shares = JSON.parse(response)
    rescue
      puts $!
      fail("Could not retrieve share list.")
    end
    shares
  end

  
  def create_upload_share(target_id, name = nil, notify_creator = false, expire_at = nil, max_slots = nil, max_size = nil, send_mail = false, mail_recipients = nil, mail_subject = nil, mail_body = nil)
    self.login_required
    
    if !target_id.is_a? Integer
      fail("Target ID must be an Integer.")
    end
    
    if name == nil
      name = SecureRandom.uuid
    end
    
    begin
      api = "/shares/uploads"
      response = RestClient.post "#{@host}#{@path}#{api}", {'targetId' => target_id, 'name' => name, 'notifyCreator' => notify_creator, 'expireAt' => expire_at, 'maxSlots' => max_slots, 'maxSize' => max_size, 'sendMail' => send_mail, 'mailRecipients' => mail_recipients, 'mailSubject' => mail_subject, 'mailBody' => mail_body}.to_json, {:content_type => :json, :accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      share = JSON.parse(response)
    rescue
      puts $!
      fail("Could not create Upload Share")
    end
    
    link = "#{@host}/#/public/shares-uploads/#{share["accessKey"]}"
    share["link"] = link
    share
  end


  def upload_shares
    self.login_required
    
    begin
      api = "/shares/uploads"
      response = RestClient.get "#{@host}#{@path}#{api}", {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      shares = JSON.parse(response)
    rescue
      puts $!
      fail("Could not retrieve share list.")
    end
    shares
  end


  def download_share_info(access_key)
    begin
      api = "/public/shares/downloads/#{access_key}"
      response = RestClient.get "#{@host}#{@path}#{api}", {:accept => :json}
      share = JSON.parse(response)
    rescue
      puts $!
    end
    share
  end
  


  def upload_share_info(access_key)
    begin
      api = "/public/shares/uploads/#{access_key}"
      response = RestClient.get "#{@host}#{@path}#{api}", {:accept => :json}
      share = JSON.parse(response)
    rescue
      puts $!
    end
    share
  end
  

  def check_password_compliance(password)
    self.login_required
    
    if password == nil
      return false
    end
    
    begin
      api = "/config/settings"
      response = RestClient.get "#{@host}#{@path}#{api}", {:accept => :json, 'X-Sds-Auth-Token' => @auth_token}
      settings = JSON.parse(response)
    rescue
      puts $!
    end
    
    allow_weak_passwords = false
    settings["items"].each do |item|
      if item["key"] == "allow_system_global_weak_password"
        if item["value"] == true
          allow_weak_passwords = true
          break
        else
          allow_weak_passwords = false
          break
        end
      end 
    end
    
    return false if password.length < 8
    return false if /[a-z]/.match(password) == nil
    return false if /[0-9]/.match(password) == nil
    return false if allow_weak_passwords == false && /[A-Z]/.match(password) == nil
    return false if allow_weak_passwords == false && /[\W]/.match(password) == nil

    return true
  end


  protected

  def login_required
    if @auth_token == nil
      fail("Login Required!")
    end
  end
  

end


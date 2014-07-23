require 'scp'

class SCPUploader

  def self.do_upload(source_files, destination, host_info)
    last_percent = 0
    last_uploaded_path = ""
    set_determinate = false
    uploaded_file_paths = []
    
    host_info = self.sanitize_host_info(host_info)
    
    self.upload(source_files, destination, host_info[:server], host_info[:port], 
                                           host_info[:username], host_info[:password]) do |percent, remote_path|
      remote_file = remote_path.split(File::SEPARATOR)[-1][0..-2]
      
      if remote_path != last_uploaded_path
        $dz.begin("Uploading #{remote_file}...")
        uploaded_file_paths << remote_path
      end
      
      last_uploaded_path = remote_path
      
      if not set_determinate
        # Switch to determinate now file sizes have been calculated and upload is beginning
        $dz.determinate(true)
        set_determinate = true
      end
      
      $dz.percent(percent) if last_percent != percent
      last_percent = percent
    end
    
    return uploaded_file_paths
  end

  def self.upload(localpaths, remotedir, host, port, user, pass, &block)
    alert_title = "SCP Upload Error"
    error_title = "Connection Failed"
    begin
      Net::SSH.start(host, user, {:password => pass, :port => port, :config => false}) do |ssh|
        remotedir = ssh.exec!("echo ~").strip if not remotedir

  	    files = []
  	    size  = 0
	
  	    localpaths.each do |localpath|
  	      path = self.path_contents(localpath, remotedir)
  	      files.concat path[:files]
  	      size += path[:size]
  	    end
  	    
  	    transferred = 0
  	    $dz.begin("Uploading #{files.size} files...") if files.length > 1 
  	    files.each do |local, remote|
  	      if local.empty? then
  	        # Try to create the directory
  	        begin
  	          ssh.exec! "mkdir \"#{remote}\""
  	        rescue
  	          # $dz.error("Error creating directory", $!)
  	          # Remote already exists?
  	        end
  	      else
  	        begin
  	          # Send the file
  	          bytesSent = 0
  	          ssh.scp.upload!(local, remote) do |ch, name, sent, total|
  	            bytesSent = sent
  	            if size != 0
  	              percent = ((transferred + sent) * 100 / size)
  	            else
  	              percent = 100
  	            end
  	            yield percent, remote
  	          end
  	          transferred += bytesSent
              rescue
                $dz.error(alert_title, $!)
  	        end
  	      end
  	    end
  	  end
  	rescue Timeout::Error
      $dz.error(alert_title, "Connection timed out.")
    rescue SocketError
      $dz.error(alert_title, "Server not found.")
    rescue Net::SSH::AuthenticationFailed
      $dz.error(alert_title, "Username or password incorrect.")
    rescue
      $dz.error(error_title, $!)
    end  
  end

  def self.path_contents(localfile, remotedir)
    files = []
    size  = 0
    filestat = File.stat(localfile)

    # Check if this is a file or directory
    if filestat.directory? then
      remotedir += ('/' + File.basename(localfile)).gsub('//', '/')
      # Make sure we create the remote directory later
      files.push ['', remotedir]
      # Recurse through dir
      Dir.foreach localfile do |file|
        next if file == '.' or file == '..'
        local = (localfile + '/' + file).gsub('//', '/')
        begin
          p = path_contents(local, remotedir)
        rescue
          next
        end
        size += p[:size]
        files.concat p[:files]
      end

    elsif filestat.file? then
      # Increment the size
      size += File.size localfile;
      remotefile = (remotedir + '/' + File.basename(localfile)).gsub('//', '/')
      files.push [localfile, "\"" + remotefile + "\""]
    end
    return { :files => files, :size => size }
  end
  
  def self.sanitize_host_info(host_info)
    host_info[:port] = (host_info[:port] != nil ? host_info[:port].to_i : 22)
    return host_info
  end
  
  def self.test_connection(host_info)
    host_info = self.sanitize_host_info(host_info)
    error_title = "Connection Failed"
    path_warning = ""
    
    begin
      Net::SSH.start(host_info[:server], host_info[:username], {:password => host_info[:password], :port => host_info[:port], :config => false }) do |ssh|
        if not ENV['remote_path']
          remote_path = ssh.exec!("echo ~").strip
          path_warning = "\n\nAs you have not specified a remote path, files will be uploaded to #{remote_path}."
        end
      end
    rescue Timeout::Error
      $dz.error(error_title, "Connection timed out.")
    rescue SocketError
      $dz.error(error_title, "Server not found.")
    rescue Net::SSH::AuthenticationFailed
      $dz.error("Authentication Failed", "Username or password incorrect.")
    rescue
      $dz.error(error_title, $!)
    end
    
    $dz.alert("Connection Successful", "SCP connection succeeded.#{path_warning}")
  end

end

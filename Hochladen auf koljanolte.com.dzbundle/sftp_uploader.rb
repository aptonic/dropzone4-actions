require 'net/scp'
require 'net/sftp'
require 'digest'

# Trying to set the locale in the SSH session causes commands to emit warnings on some servers
ENV.delete('LC_ALL')

def encode_url(old_remote_path)
    remote_path           = old_remote_path.to_s #'/home/kolja/www/temp/d.txt'
    remote_file_name      = File.basename(remote_path)
    remote_file_extension = File.extname(remote_file_name)
    md5                   = Digest::MD5.new
    md5_string            = md5.update remote_file_name
    md5_string            = md5.hexdigest.to_s
    new_remote_file_name  = md5_string[1..8] + remote_file_extension
    new_remote_file_name  = remote_path.sub remote_file_name, new_remote_file_name
    new_remote_file_name  = new_remote_file_name.to_s
end

class SFTPUploader

    def self.do_upload(source_files, destination, host_info)
        last_percent        = 0
        last_uploaded_path  = ""
        set_determinate     = false
        uploaded_file_paths = []
        host_info           = self.sanitize_host_info(host_info)

        self.upload(source_files, destination, host_info[:server], host_info[:port],
                    host_info[:username], host_info[:password]) do |percent, remote_path|
            remote_file = remote_path.split(File::SEPARATOR)[-1]

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
        alert_title = "SFTP Upload Error"
        error_title = "Connection Failed"
        begin
            # If using public key auth then attempt connection so that ssh-agent caches private key
            puts `ssh -p #{port} #{host} 'exit'` if not pass

            session = Net::SSH.start(host, user, {:password => pass, :port => port})

            Net::SFTP::Session.new(session).connect! do |sftp|
                remotedir = "" if not remotedir

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
                    remote = encode_url(remote)

                    if local.empty? then
                        # Try to create the directory
                        begin
                            sftp.mkdir(remote)
                        rescue => e
                            $dz.error("Error creating directory", e.message)
                        end
                    else
                        begin
                            # Send the file
                            bytesSent    = 0
                            totalWritten = 0
                            sftp.upload!(local, remote) do |event, uploader, *args|
                                if event == :put
                                    totalWritten += args[2].length
                                    bytesSent    = totalWritten
                                    if size != 0
                                        percent = ((transferred + totalWritten) * 100 / size)
                                    else
                                        percent = 100
                                    end
                                    yield percent, local
                                end
                            end
                            transferred += bytesSent
                        rescue => e
                            $dz.error(alert_title, e.message)
                        end
                    end
                end
            end
        rescue Timeout::Error
            $dz.error(error_title, "Connection timed out.")
        rescue SocketError
            $dz.error(error_title, "Server not found.")
        rescue Net::SSH::AuthenticationFailed
            $dz.error("Authentication Failed", "Username or password incorrect.")
        rescue => e
            if e.message =~ /PKey/
                $dz.error(error_title, "Your private key could not be unlocked.\n\nTry SSHing to the server from Terminal to unlock the keychain then try your upload again.")
            elsif e.message =~ /ioctl/
                if not pass then
                    $dz.error(error_title, "Public key authorization failed and you have not provided a password.")
                else
                    $dz.error(error_title, "Public key authorization failed and the password you provided was not accepted.")
                end
            else
                $dz.error(error_title, e.message)
            end
        end
    end

    def self.path_contents(localfile, remotedir)
        files    = []
        size     = 0
        filestat = File.stat(localfile)

        # Check if this is a file or directory
        if filestat.directory? then
            leading_slash = (remotedir == '' ? "" : "/")
            remotedir     += (leading_slash + File.basename(localfile)).gsub('//', '/')
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
            leading_slash = (remotedir == '' ? "" : "/")
            remotedir     += (leading_slash + File.basename(localfile)).gsub('//', '/')
            size          += File.size localfile
            files.push [localfile, remotedir]
        end
        return {:files => files, :size => size}
    end

    def self.sanitize_host_info(host_info)
        host_info[:port] = (host_info[:port] != nil ? host_info[:port].to_i : 22)
        return host_info
    end

    def self.test_connection(host_info)
        host_info    = self.sanitize_host_info(host_info)
        error_title  = "Connection Failed"
        path_warning = ""

        # If using public key auth then attempt connection so that ssh-agent caches private key
        puts `ssh -p #{host_info[:port]} #{host_info[:server]} 'exit'` if not host_info[:password]

        begin
            Net::SSH.start(host_info[:server], host_info[:username], {:password => host_info[:password], :port => host_info[:port]})
        rescue Timeout::Error
            $dz.error(error_title, "Connection timed out.")
        rescue SocketError
            $dz.error(error_title, "Server not found.")
        rescue Net::SSH::AuthenticationFailed
            $dz.error("Authentication Failed", "Username or password incorrect.")
        rescue => e
            if e.message =~ /PKey/
                $dz.error(error_title, "Your private key could not be unlocked.\n\nTry SSHing to the server from Terminal to unlock the keychain then try your upload again.")
            elsif e.message =~ /ioctl/
                if not host_info[:password] then
                    $dz.error(error_title, "Public key authorization failed and you have not provided a password.")
                else
                    $dz.error(error_title, "Public key authorization failed and the password you provided was not accepted.")
                end
            else
                $dz.error(error_title, e.message)
            end
        end

        $dz.alert("Connection Successful", "SFTP connection succeeded.")
    end

end
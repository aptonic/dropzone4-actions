require 'aws-sdk-v1'

class S3

  def configure_client
    AWS.config(:access_key_id => ENV['access_key_id'], 
               :secret_access_key => ENV['access_secret'], 
               :s3_endpoint => ENV['server'].sub(/^https:\/\/|http:\/\//, ''),
               :s3_force_path_style => true,
               :proxy_uri => get_proxy)
     
    @aws = AWS::S3.new
  end

  def get_proxy
    e = ENV['https_proxy']
    if e && !e.empty?
      if !e.start_with? "http"
        e = "https://#{e}"
      end
    end
    return e
  end

  def upload_file(file_path, bucket, &block)
    file = File.open(file_path, 'r', encoding: 'BINARY')
  
    basename = File.basename(file_path)
    upload_path = basename
  
    if ENV['folder'] != nil
      slash = (ENV['folder'][-1,1] == "/" ? "" : "/")
      upload_path = ENV['folder'] + slash + basename
    end

    self.check_bucket_access(bucket, bucket)
    upload_path = self.get_unique_upload_path(upload_path, bucket)

    mime_type = `file -b --mime-type \"#{file_path}\"`.strip

    opts = {
      content_type: mime_type,
      estimated_content_length: file.size,
      acl: :public_read
    }

    part_size = self.compute_part_size(opts)

    parts_number = (file.size.to_f / part_size).ceil.to_i
    obj          = bucket.objects[upload_path]

    upload_progress = 0

    begin
      obj.multipart_upload(opts) do |upload|
        until file.eof? do
          break if (abort_upload = upload.aborted?)

          upload.add_part(file.read(part_size))
          upload_progress += 1.0 / parts_number

          # Yields the Float progress and the String filepath from the
          # current file that's being uploaded
          yield((upload_progress * 100).to_i, upload) if block_given?
        end
      end
    end
    
    file.close
    
    File.basename(upload_path)
  end

  def compute_part_size(options)
    max_parts = 10000
    min_size  = 5242880 #5 MB
    estimated_size = options[:estimated_content_length]

    [(estimated_size.to_f / max_parts).ceil, min_size].max.to_i
  end
  
  def get_bucket
    bucket_name = ENV['bucket_name'].downcase
    bucket = @aws.buckets[bucket_name]

    begin
      bucket_exists = bucket.exists?
    rescue SocketError
      $dz.error("Connection Failed", "Check the S3 server (endpoint) is set correctly and check your network connection.\n\nDebug Info:: #{$!}")
    rescue AWS::S3::Errors::PermanentRedirect
      $dz.error("Incorrect Server for this Bucket", "The bucket you are trying to access is not available using the server you have set. Please update the server to the correct endpoint.\n\nYou can find the correct endpoint at\nhttp://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region")
    rescue Exception => e
      puts e.inspect
      $dz.error("Failed to access bucket '#{bucket_name}'", e.to_s)
    end
      
    begin
      bucket = @aws.buckets.create(bucket_name) unless bucket_exists
    rescue Exception => e
      $dz.error("Failed to create bucket '#{bucket_name}'", e.to_s)
      $dz.url(false)
    end
    
    bucket
  end
  
  def check_bucket_access(bucket, upload_path)
    begin
      bucket.objects[upload_path].exists?
    rescue AWS::S3::Errors::Forbidden
      $dz.error("Access to the specified bucket was forbidden", "Check your Access Key ID and Secret are correct and you have permission to access the specified bucket.\n\nIf you enter a new bucket name it will be created on your first upload. Bucket names must be unique.")
    rescue Exception => e
      $dz.error("Failed to access bucket", e.to_s)
    end
  end
  
  def get_unique_upload_path(upload_path, bucket)
    count = 1
    number = ""
    
    while true
      no_ext = upload_path.chomp(File.extname(upload_path))
      unique_path = no_ext + number + File.extname(upload_path)
      break if not bucket.objects[unique_path].exists?
      number = "-#{count}"
      count = count + 1
    end
    
    unique_path
  end
end
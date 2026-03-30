# Dropzone Action Info
# Name: Paperless-ngx
# Description: Uploads documents to a Paperless-ngx server.\n\nServer - your Paperless URL (e.g. paperless.example.com)\nPort - only needed for non-default ports, otherwise leave blank\nUsername/Password - your Paperless credentials, OR enter "api" as username and your API token as password\nRemote Path and Root URL - leave blank (not used)
# Handles: Files
# Creator: Jason Learst
# URL: https://github.com/jasonlearst/Paperless-ngx-Dropzone-Action
# Events: Dragged, Clicked, TestConnection
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.1
# MinDropzoneVersion: 4.0
# OptionsNIB: ExtendedLogin
# UniqueID: 85247204
# OptionsTitle: Paperless-ngx Connection

require 'net/http'
require 'uri'
require 'json'
require 'stringio'

# IO wrapper that reports upload progress to Dropzone
class ProgressIO
  def initialize(io, total_size, bytes_offset, overall_total, &on_progress)
    @io = io
    @total_size = total_size
    @bytes_offset = bytes_offset
    @overall_total = overall_total
    @bytes_read = 0
    @on_progress = on_progress
    @last_percent = -1
  end

  def read(length = nil, buf = nil)
    data = buf ? @io.read(length, buf) : @io.read(length)
    if data
      @bytes_read += data.bytesize
      percent = ((@bytes_offset + @bytes_read) * 100.0 / @overall_total).to_i
      percent = [percent, 100].min
      if percent != @last_percent
        @on_progress.call(percent)
        @last_percent = percent
      end
    end
    data
  end

  def size
    @total_size
  end
end

def dragged
  files = validate_files($items)

  $dz.begin("Uploading #{files.length} document#{files.length > 1 ? 's' : ''} to Paperless...")
  $dz.determinate(true)

  total_size = files.sum { |f| File.size(f) }
  bytes_uploaded = 0
  uploaded = []

  files.each do |file|
    filename = File.basename(file)
    $dz.begin("Uploading #{filename}...")
    upload_document(file, bytes_uploaded, total_size)
    bytes_uploaded += File.size(file)
    uploaded << filename
  end

  $dz.finish("Uploaded #{uploaded.length} document#{uploaded.length > 1 ? 's' : ''}")
  $dz.url(false)
rescue => e
  $dz.fail("Error: #{e.message}")
end

def clicked
  url = server_url
  system("open", url)
  $dz.finish("Opened Paperless")
  $dz.url(false)
rescue => e
  $dz.fail("Error: #{e.message}")
end

def test_connection
  username = ENV['username']
  password = ENV['password']

  if username.nil? || username.strip.empty? || password.nil? || password.strip.empty?
    $dz.error("Configuration Error", "Username and password are required.")
    return
  end

  uri = URI.parse("#{server_url}/api/documents/?page_size=1")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == "https")
  http.open_timeout = 10
  http.read_timeout = 10

  request = Net::HTTP::Get.new(uri.request_uri)
  if username.strip.downcase == "api"
    request["Authorization"] = "Token #{password.strip}"
  else
    request.basic_auth(username.strip, password.strip)
  end

  response = http.request(request)

  if response.code.to_i >= 200 && response.code.to_i < 300
    $dz.alert("Connection Successful", "Successfully connected to Paperless-ngx at #{server_url}")
  elsif response.code.to_i == 401 || response.code.to_i == 403
    $dz.error("Authentication Failed", "Username or password incorrect.")
  else
    $dz.error("Connection Failed", "Server returned HTTP #{response.code}.")
  end
rescue Timeout::Error
  $dz.error("Connection Failed", "Connection timed out. Check your server address and port.")
rescue SocketError
  $dz.error("Connection Failed", "Server not found. Check your server address.")
rescue => e
  $dz.error("Connection Failed", e.message)
end

def server_url
  url = ENV['server']
  if url.nil? || url.strip.empty?
    $dz.fail("Server URL not configured. Edit the action settings to set it.")
  end
  url = url.strip
  url = "https://#{url}" unless url.start_with?("http://", "https://")
  url.chomp!("/")

  port = ENV['port']
  if port && !port.strip.empty?
    uri = URI.parse(url)
    default_port = (uri.scheme == "https") ? 443 : 80
    if port.strip.to_i != default_port
      # Only add port if not already included in the server URL
      unless url.match?(/:\d+$/) || url.match?(/:\d+\//)
        uri.port = port.strip.to_i
        url = uri.to_s
      end
    end
  end

  url
end

def validate_files(items)
  missing = items.select { |f| !File.exist?(f) }
  unless missing.empty?
    names = missing.map { |f| File.basename(f) }.join(", ")
    $dz.fail("File not found: #{names}")
  end

  items
end

def upload_document(file_path, bytes_offset, overall_total)
  username = ENV['username']
  password = ENV['password']

  if username.nil? || username.strip.empty? || password.nil? || password.strip.empty?
    $dz.fail("Credentials not configured. Edit the action settings.")
  end

  uri = URI.parse("#{server_url}/api/documents/post_document/")
  boundary = "----DZPaperless#{rand(1_000_000_000)}"
  filename = File.basename(file_path)

  body = build_multipart_body(boundary, file_path, filename)

  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == "https")
  http.open_timeout = 15
  http.read_timeout = 120

  request = Net::HTTP::Post.new(uri.request_uri)
  request["Content-Type"] = "multipart/form-data; boundary=#{boundary}"

  if username.strip.downcase == "api"
    request["Authorization"] = "Token #{password.strip}"
  else
    request.basic_auth(username.strip, password.strip)
  end

  body_io = ProgressIO.new(StringIO.new(body), body.bytesize, bytes_offset, overall_total) do |percent|
    $dz.percent(percent)
  end
  request.body_stream = body_io
  request["Content-Length"] = body.bytesize.to_s

  response = http.request(request)

  unless response.code.to_i >= 200 && response.code.to_i < 300
    $dz.fail("Upload failed (#{response.code}): #{response.body}")
  end
end

def build_multipart_body(boundary, file_path, filename)
  body = ""
  body << "--#{boundary}\r\n"
  body << "Content-Disposition: form-data; name=\"document\"; filename=\"#{filename}\"\r\n"
  body << "Content-Type: application/octet-stream\r\n"
  body << "\r\n"
  body << File.binread(file_path)
  body << "\r\n"
  body << "--#{boundary}--\r\n"
  body
end

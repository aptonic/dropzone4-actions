# Dropzone Action Info
# Name: Gokapi
# Description: Uploads files to a Gokapi server and copies the share URL to the clipboard.\n\nServer - your Gokapi URL (e.g. share.example.com)\nPort - only needed for non-default ports, otherwise leave blank\nUsername - enter "api" (placeholder; not used, but Dropzone requires a value before Test Connection will run)\nPassword - your Gokapi API key (must have UPLOAD permission)\nRemote Path and Root URL - leave blank (not used)\n\nHold Shift while dragging to set per-upload expiry, download limit, and password.
# Handles: Files
# Creator: Jason Learst
# URL: https://github.com/jasonlearst/Gokapi-Dropzone-Action
# Events: Dragged, Clicked, TestConnection
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.1
# MinDropzoneVersion: 4.0
# OptionsNIB: ExtendedLogin
# UniqueID: 73914820
# OptionsTitle: Gokapi Connection

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

  opts = {}
  if shift_held?
    opts = prompt_upload_options
  end

  $dz.begin("Uploading #{files.length} file#{files.length > 1 ? 's' : ''} to Gokapi...")
  $dz.determinate(true)

  total_size = files.sum { |f| File.size(f) }
  bytes_uploaded = 0
  download_urls = []

  files.each do |file|
    filename = File.basename(file)
    $dz.begin("Uploading #{filename}...")
    url = upload_file(file, bytes_uploaded, total_size, opts)
    download_urls << url
    bytes_uploaded += File.size(file)
  end

  if download_urls.length == 1
    $dz.finish("Uploaded — share URL copied")
    $dz.url(download_urls.first)
  else
    $dz.finish("Uploaded #{download_urls.length} files — share URLs copied")
    $dz.text(download_urls.join("\n"))
  end
rescue => e
  $dz.fail("Error: #{e.message}")
end

def clicked
  url = "#{server_url}/admin"
  system("open", url)
  $dz.finish("Opened Gokapi")
  $dz.url(false)
rescue => e
  $dz.fail("Error: #{e.message}")
end

def test_connection
  api_key = ENV['password']

  if api_key.nil? || api_key.strip.empty?
    $dz.error("Configuration Error", "API key is required. Paste your Gokapi API key into the Password field.")
    return
  end

  uri = URI.parse("#{server_url}/api/info/config")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == "https")
  http.open_timeout = 10
  http.read_timeout = 10

  request = Net::HTTP::Get.new(uri.request_uri)
  request["apikey"] = api_key.strip
  request["Accept"] = "application/json"

  response = http.request(request)

  if response.code.to_i >= 200 && response.code.to_i < 300
    $dz.alert("Connection Successful", "Successfully connected to Gokapi at #{server_url}")
  elsif response.code.to_i == 401 || response.code.to_i == 403
    $dz.error("Authentication Failed", "API key is invalid or missing the UPLOAD permission.")
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

def shift_held?
  mods = ENV['KEY_MODIFIERS'].to_s
  mods.include?("Shift")
end

def prompt_upload_options
  pconfig = <<~PASHUA
    *.title = Gokapi Upload Options
    intro.type = text
    intro.text = Leave any field blank to use the server default. Set Expiry or Downloads to 0 for unlimited.
    expiry.type = textfield
    expiry.label = Expiry (days) — default 14
    expiry.width = 320
    downloads.type = textfield
    downloads.label = Allowed downloads — default 1
    downloads.width = 320
    password.type = textfield
    password.label = Password (optional)
    password.width = 320
    b.type = defaultbutton
    b.label = Upload
    cb.type = cancelbutton
    cb.label = Cancel
  PASHUA

  result = $dz.pashua(pconfig)

  if result['cb'] == '1'
    $dz.fail("Upload cancelled")
  end

  opts = {}
  opts[:expiryDays] = result['expiry'].strip if result['expiry'] && !result['expiry'].strip.empty?
  opts[:allowedDownloads] = result['downloads'].strip if result['downloads'] && !result['downloads'].strip.empty?
  opts[:password] = result['password'] if result['password'] && !result['password'].to_s.empty?
  opts
end

def upload_file(file_path, bytes_offset, overall_total, opts = {})
  api_key = ENV['password']

  if api_key.nil? || api_key.strip.empty?
    $dz.fail("API key not configured. Paste your Gokapi API key into the Password field.")
  end

  uri = URI.parse("#{server_url}/api/files/add")
  boundary = "----DZGokapi#{rand(1_000_000_000)}"
  filename = File.basename(file_path)

  body = build_multipart_body(boundary, file_path, filename, opts)

  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == "https")
  http.open_timeout = 15
  http.read_timeout = 600

  request = Net::HTTP::Post.new(uri.request_uri)
  request["Content-Type"] = "multipart/form-data; boundary=#{boundary}"
  request["apikey"] = api_key.strip
  request["Accept"] = "application/json"

  body_io = ProgressIO.new(StringIO.new(body), body.bytesize, bytes_offset, overall_total) do |percent|
    $dz.percent(percent)
  end
  request.body_stream = body_io
  request["Content-Length"] = body.bytesize.to_s

  response = http.request(request)

  unless response.code.to_i >= 200 && response.code.to_i < 300
    $dz.fail("Upload failed (#{response.code}): #{response.body}")
  end

  parsed = JSON.parse(response.body)
  download_url = parsed.dig("FileInfo", "UrlDownload")

  if download_url.nil? || download_url.empty?
    $dz.fail("Upload succeeded but server response did not include a download URL.")
  end

  download_url
end

def build_multipart_body(boundary, file_path, filename, opts = {})
  body = String.new(encoding: "ASCII-8BIT")

  opts.each do |key, value|
    body << "--#{boundary}\r\n"
    body << "Content-Disposition: form-data; name=\"#{key}\"\r\n"
    body << "\r\n"
    body << value.to_s.dup.force_encoding("ASCII-8BIT")
    body << "\r\n"
  end

  body << "--#{boundary}\r\n"
  body << "Content-Disposition: form-data; name=\"file\"; filename=\"#{filename}\"\r\n"
  body << "Content-Type: application/octet-stream\r\n"
  body << "\r\n"
  body << File.binread(file_path)
  body << "\r\n"
  body << "--#{boundary}--\r\n"
  body
end

# Dropzone Action Info
# Name: Up1
# Description: Sends the clipboard or any dropped text or file content to the Up1 service (https://up1.ca) and puts the URL on the clipboard. Data are encrypted thanks to the SJCL AES-CCM encryption ported to Ruby by Mark Percival (https://github.com/mdp/sjcl_rb). Due to the limitation of the encryption library, all operations are achieves in memory, therefore uploading very large file is NOT recommended.
# Handles: Files, Text
# Creator: Denis Gervalle (SOFTEC sa)
# URL: http://softec.lu
# Events: Clicked, Dragged
# SkipConfig: Yes
# RunsSandboxed: Yes
# UniqueID: 2175601
# Version: 1.1
# MinDropzoneVersion: 3.0
# RubyPath: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/bin/ruby

require 'rubygems'
require './bundler/setup'
require 'openssl'
require 'base64'
require 'securerandom'
require 'net/http'
require 'net/https'
require 'uri'
require 'cgi'
require 'json'

module SJCL
require 'sjcl/bit_array'
require 'sjcl/codec_string'
require 'sjcl/codec_base64'
require 'sjcl/codec_hex'
require 'sjcl/aes'
require 'sjcl/ccm'
end

DEFAULT_URL = 'https://up1.ca/'
API_KEY = 'c61540b5ceecd05092799f936e27755f'
BOUNDARY = "0123456789ABLEWASIEREISAWELBA9876543210"
HEADER = { "Content-Type" => "multipart/form-data; boundary=#{ BOUNDARY }",
           "User-Agent" => "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Dropzone/3.0 Ruby/2.0" }

def dragged
  $dz.determinate(false)
  mimetype = 'text/plain'
  basename = 'Pasted.txt'

  if !@input
    case ENV['dragged_type']
      when 'files'
        $dz.begin("Loading file...")
        filename = $items[0]
        @input =  open(filename).read
        mimetype = `file -b --mime-type #{filename.gsub(/ /,"\\ ")}`.gsub(/\n/,"")
        basename = File.basename(filename)
      when 'text'
        @input = $items[0]
    end
  end

  $dz.begin("Encrypting data...")
  
  header = {
    :mime => mimetype,
    :name => basename
  }
  
  data, seed, ident = encrypt(header, @input)
  
  $dz.begin("Uploading to Up1...")

  response = http_post(data, {"api_key" => API_KEY, "ident" => ident})
  if response.is_a?(Net::HTTPOK)
    data = response.body
    if data =~ /^\{"delkey":".*"\}\s*$/m then
      delkey = data.gsub(/^\{"delkey":"/m, "").gsub(/"\}\s*$/m, "")
      $dz.finish("URL copied to clipboad...")
      $dz.save_value('deleteurl', "#{server}/del?delkey=#{delkey}&ident=#{ident}")
      $dz.text("#{server}/\##{seed}")
    else
      $dz.error("Failure parsing response from Up1", data)
    end
  else
    $dz.error("Failure uploading to Up1", response.code)
  end
 
rescue Errno::ECONNREFUSED => e
  $dz.error("No connection to Up1", e.message)
end

def clicked
  @input = $dz.read_clipboard
  if @input.empty?
    system("open #{server}")
  else
    dragged
  end
end

def encrypt(header, data, opts = {})
  aes_encrypt(
    SJCL::Codec::UTF8String.toBits(header.to_json.encode("UTF-16BE").force_encoding("UTF-8") + "\0\0" + data),
    opts
  )
end

def http_post(data, params)
  uri = URI.parse server
  data, headers = prepareRequest(data, params)

  http = Net::HTTP.new uri.host, uri.port
  if uri.scheme =~ /^https/
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  end
  http.start {|con| con.post('/up', data, headers)}
end

def aes_encrypt(data, opts = {})
  seed = opts[:key] || generateSeed(opts[:keylen] || 16)
  key, iv, ident = getParameters(seed)
  cipher = SJCL::Cipher::AES.new(key)
  adata = SJCL::Codec::UTF8String.toBits('')
  data = SJCL::Mode::CCM.encrypt(cipher, data, iv, adata)
  [ SJCL::Codec::UTF8String.fromBits(data),
    Base64.urlsafe_encode64(seed).gsub("=", ""),
    SJCL::Codec::Base64.fromBits(ident).gsub("=", "").gsub("+", "-").gsub("/", "_") ]
end

def getParameters(seed)
  key = OpenSSL::Digest::SHA512.digest(seed)
  hash = SJCL::Codec::UTF8String.toBits(key)
  [ SJCL::BitArray.bitSlice(hash, 0, 256),
    SJCL::BitArray.bitSlice(hash, 256, 384),
    SJCL::BitArray.bitSlice(hash, 384, 512) ]
end

def generateSeed(len = 16)
  SecureRandom.random_bytes(len)
end

def server
  return @server if @server
  @server = DEFAULT_URL.dup
  @server.chop! if server.end_with?('/')
  @server
end

def prepareRequest(data, params)
  fp = []
  params.each do |k, v|
    fp.push("Content-Disposition: form-data; name=\"#{CGI::escape(k)}\"\r\n\r\n#{v}\r\n")
  end
  fp.push("Content-Disposition: form-data; name=\"file\"; filename=\"blob\"\r\nContent-Type: application/octet-stream\r\n\r\n#{ data }\r\n")
  return fp.collect {|p| "--" + BOUNDARY + "\r\n" + p }.join("") + "--" + BOUNDARY + "--", HEADER
end
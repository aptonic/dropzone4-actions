# Dropzone Action Info
# Name: Goo.gl
# Description: Dropped URL will be converted to a short Goo.gl URL.\n\nTo use without authentication, leave the username and password fields blank.\n
# Handles: Text
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# Events: Clicked, Dragged
# OptionsNIB: Login
# SkipValidation: Yes
# RunsSandboxed: No
# LoginTitle: Google Login Details
# Version: 1.0
# MinDropzoneVersion: 3.2.1
# UniqueID: 1024

require 'cgi'
require 'rexml/document'
require 'uri'
require 'net/http'
require 'net/https'
require 'json'

def dragged
	shorten($items[0])
end

def shorten(item)
	$dz.determinate(false)
	$dz.begin("Getting Goo.gl URL")
	
	if item =~ /http/
		username = ENV['username']
		password = ENV['password']

		if item =~ /http:\/\/goo.gl\//
			#-------------------------------------------------------------
			# Try to Expand Shortened URL
			#-------------------------------------------------------------
			urlToExpand = CGI::escape(item)
			expandURL = URI.parse("https://www.googleapis.com/urlshortener/v1/url?shortUrl=#{urlToExpand}")
			https = Net::HTTP.new(expandURL.host,expandURL.port)
			https.use_ssl = true
			req = Net::HTTP::Get.new(expandURL.to_s)
			res = https.request(req)
			expandedURL = JSON.parse(res.body)['longUrl']||0;
			puts(res.body)

			if expandedURL == 0
				# Failed Expand URL
				errorCode = JSON.parse(res.body)['error']['code']||0
				errorResponse = JSON.parse(res.body)['error']['message']
				if errorCode != 0
					$dz.alert("Goo.gl Failed to Expand URL", "#{errorCode} #{errorResponse}")
				end
				$dz.finish("Expand URL Failed")
			else
				# Expand URL
				$dz.url(expandedURL)
				$dz.alert("Goo.gl expanded URL for #{item}", "#{expandedURL}")
				$dz.finish("Goo.gl expanded URL for #{item} is now on clipboard")
			end
			
		else
			#-------------------------------------------------------------
			# Shorten URL With Goo.gl
			#-------------------------------------------------------------
			if username.length > 10
				# Get Authentification Token
				puts "Password defined, user #{username}"

				service = 'urlshortener'  
				source = 'dropzone-googl-1.0'  
				path = '/accounts/ClientLogin'  
		  
				data = ["accountType=HOSTED_OR_GOOGLE",   
		        "Email=#{username}",  
		        "Passwd=#{password}",  
		        "service=#{service}",  
		        "source=#{source}"].join('&') 

				http = Net::HTTP.new(host='www.google.com', port=443)  
				http.use_ssl = true  
				http.start  
				  
				headers = {'Content-Type' => 'application/x-www-form-urlencoded'}  
				resp, data = http.post(path, data, headers)  
				token = data[/Auth=(.*)/, 1]  # parse out the Auth token  

				reqHeader = {"Content-Type"=>"application/json","Authorization"=>"GoogleLogin auth=#{token}"}

			else
				# Shorten URL without authentification
				puts 'Password not defined'
				reqHeader = {'Content-Type' =>'application/json'}
			end

			uri = URI.parse("https://www.googleapis.com/urlshortener/v1/url")
			https = Net::HTTP.new(uri.host,uri.port)
			https.use_ssl = true
			req = Net::HTTP::Post.new(uri.path, reqHeader) 
			req.body = '{ "longUrl" : "'+item+'" }'
			res = https.request(req)
			# puts "Response #{res.code} #{res.message}: #{res.body}"
			
			shortcutURL = JSON.parse(res.body)['id']||0
			if shortcutURL != 0
				$dz.finish("Goo.gl Shortened URL is now on clipboard")
				$dz.url( shortcutURL )
			else
				errorMessage = JSON.parse(res.body)['error']['message']||''
				$dz.finish("Goo.gl failed to shortcut your URL : #{errorMessage}")
				$dz.url(false)
			end
			puts(res.body)
		end
	else
		$dz.finish("Invalid URL")
		$dz.url(false)
	end
end

def readClipboard
	IO.popen('pbpaste') {|clipboard| clipboard.read}
end
 
def clicked
	data = readClipboard()
	shorten(data)
end
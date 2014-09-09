# Dropzone Action Info
# Name: Pushover
# Description: Send clipboard content via Pushover (https://pushover.net/).
# Creator: Dominique Da Silva
# URL: http://www.agonia.fr
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# Handles: Text
# OptionsNIB: APIKey
# LoginTitle: Pushover User API Key

# require 'net/http'
require 'net/https'
require 'uri'

def send(data)

	$dz.begin("Sending clipboard content via Pushover")

	url = URI.parse("https://api.pushover.net/1/messages")
	req = Net::HTTP::Post.new(url.path)
	api_key = ENV['api_key']
	message = data[0,600].strip()

	if message.length < 5 || message.nil? || message.empty?
		$dz.error("Nothing to send", "Your clipboard is empty.")
	end

	req.set_form_data({
		:token => "aAAXwYRyTCJr4W7i7JtabmSmtgUf7f",
		:user => "#{api_key}",
		:message => "#{message}",
	})
	res = Net::HTTP.new(url.host, url.port)
	res.use_ssl = true
	res.verify_mode = OpenSSL::SSL::VERIFY_PEER
	res.start {|http| http.request(req) }

end

def readClipboard
	IO.popen('pbpaste') {|clipboard| clipboard.read}
end

def dragged
	if ENV['dragged_type'] == 'text'
		send($items[0])
		$dz.finish("Dragged content sent via Pushover")
	end
	$dz.url(false)
end

def clicked
	# This method gets called when a user clicks on your action
	data = readClipboard()

	if ENV['api_key'] == ''
		$dz.error("User Key Empty", "You must define your user key.")
	else
		send(data)
		$dz.finish("Clipboard content sent via Pushover")
	end
	$dz.url(false)
end

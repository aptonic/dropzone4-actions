# Dropzone Action Info
# Name: Boxcar
# Description: Send message to Boxcar App (https://boxcar.io/).
# Creator: Dominique Da Silva
# URL: https://inspira.io
# Events: Clicked, Dragged
# SkipConfig: No
# Handles: Text
# OptionsNIB: APIKey
# LoginTitle: Boxcar User API Key
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# Version: 1.0
# UniqueID: 7000

require 'notification'

def send(data)

	$dz.begin("Sending message via Boxcar")

	notification = Notification.new('boxcar', ENV['api_key'])
	notification.message = data.chomp
	notification.sound = 'beep-soft'

	notification.push

end

def readClipboard
	IO.popen('pbpaste') {|clipboard| clipboard.read}
end

def dragged
	if ENV['dragged_type'] == 'text'
		send($items[0])
		$dz.finish("Message sent via Boxcar")
	end
	$dz.url(false)
end

def clicked
	system("open https://new.boxcar.io/account")
end

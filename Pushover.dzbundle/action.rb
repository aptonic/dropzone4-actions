# Dropzone Action Info
# Name: Pushover
# Description: Send message via a Pushover notification (https://pushover.net/). Hold Alt Key to select a device or Shift Key to refresh devices list.
# Creator: Dominique Da Silva
# URL: https://inspira.io
# Events: Clicked, Dragged
# KeyModifiers: Option, Shift
# SkipConfig: No
# Handles: Text
# OptionsNIB: APIKey
# LoginTitle: Pushover User API Key
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# Version: 1.1
# UniqueID: 7002

require 'notification'

def send(data)

	$dz.begin("Sending message via Pushover")

	ask_device = ENV['ask_device']
	devices = ENV['devices']
	modifier = ENV['KEY_MODIFIERS']

	notification = Notification.new('pushover', ENV['api_key'])
	notification.message = data.chomp
	notification.sound = 'none'

	# Ask user if he want to display a list of device each time
	if ask_device.nil?
		output = $dz.cocoa_dialog('msgbox --no-cancel --title "Pushover" --text "Send notification to all devices by default ?" --informative-text "To select a device later, you can hold Shift Key to display the list of device." --button1 "Yes to all" --button2 "No, choose each time" ')
		if output == "2\n"
			$dz.save_value('ask_device', 'true')
			ask_device = 'true'
		else
			$dz.save_value('ask_device', 'false')
			ask_device = 'false'
		end
	end

	# DISPLAY A LIST OF DEVICES
	# Option: Display the dropdown list
	# Shift: Update the devices from Pushover server and open the dropdown list

	# Refresh user devices list from Pushover
	if devices.nil? || modifier == 'Shift'
		devices = notification.pushover_devices
	end

	if ( ask_device == 'true' || modifier == 'Option' || modifier == 'Shift' ) && ! devices.nil?
		devices_list = devices.tr(',',' ')
		output = $dz.cocoa_dialog("dropdown --title 'Pushover' --no-cancel --text \"Select the device in the list to which to send the message.\" --float --button1 'Send' --string-output --items #{devices_list}")
		button, device = output.split("\n")
		puts "Selected device: "+device
		notification.device = device
	end

	notification.push # send the message

	$dz.finish("Message sent via Pushover")
	$dz.url(false)
end

def dragged
	send($items[0])
end

def clicked

	# Clicked action open Pushover webpage
	po_website = ["https://pushover.net/","https://client.pushover.net/"]
	website_choice = ENV['website_choice']

	if website_choice.nil?
		website_choice = "0"
		choice = $dz.cocoa_dialog('msgbox --title "Pushover Website" --text "Choose the Pushover webpage to open by default." --informative-text "For Pushover Desktop Users you can choose the client website when you click on the action, otherwire select the homepage." --button3 "Cancel" --button2 "Pushover Client" --button1 "Pushover homepage"')
		choice = choice.to_i - 1

		if choice == 0 or choice == 1 then
			website_choice = choice.to_s
			$dz.save_value('website_choice', choice)
		end
	end

	choice = website_choice.to_i
	puts "Open website "+po_website[choice]
	system("open "+po_website[choice])

	# update devices
	notification = Notification.new('pushover', ENV['api_key'])
	notification.pushover_devices

end

# Dropzone Action Info
# Name: Pushover
# Description: Send message via a Pushover notification (https://pushover.net/). Hold Alt Key to select a device, Shift Key to refresh devices list and Command key to reset settings.
# Creator: Dominique Da Silva
# URL: https://apps.inspira.io
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Shift
# SkipConfig: No
# Handles: Text
# OptionsNIB: APIKey
# LoginTitle: Pushover User API Key
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# Version: 1.2
# UniqueID: 7002

require 'notification'

@po_website = ["https://pushover.net/","https://client.pushover.net/"]

def send(data)

	$dz.begin("Sending message via Pushover")

	ask_device = ENV['ask_device']
	devices = ENV['devices']
	modifier = ENV['KEY_MODIFIERS']

	notification = Notification.new('pushover', ENV['api_key'])
	notification.message = data.chomp
	notification.sound = 'none'

	# Ask user if he want to display a list of device each time
	if ask_device.nil? || modifier == 'Command'
		pconfig = "
			*.title = Pushover
			txt.type = text
			txt.default = [return]To select a device later, you can hold Alt Key to display the list of device.
			txt.label = Send notification to all devices by default ?
			b1.type = defaultbutton
			b1.label = Yes to all
			cb.type = cancelbutton
			cb.label = No, choose each time
		"
		result = $dz.pashua(pconfig)

		if result['b1'] == '1'
			$dz.save_value('ask_device', 'false')
			ask_device = 'false'
		else
			$dz.save_value('ask_device', 'true')
			ask_device = 'true'
		end

		if modifier == 'Command'
			select_prefered_website()
		end
	end

	# DISPLAY A LIST OF DEVICES
	# Option: Display the list to select a device
	# Shift: Update the devices from Pushover server and open the dropdown list
	# Command: Reset user settings and prompt again

	# Refresh user devices list from Pushover
	if devices.nil? || modifier == 'Shift'
		devices = notification.pushover_devices
	end

	if ( ask_device == 'true' || modifier == 'Option' || modifier == 'Shift' ) && ! devices.nil?
		send_to_all_title = "All devices"
		# Generate devices radio options
		radio_options = ""
		devices.split(',').each { |device|
			radio_options = "#{radio_options}\ndevice.option = #{device}"
		}
		pconfig = "
			*.title = Pushover
			device.type = radiobutton
			#{radio_options}
			device.option = #{send_to_all_title}
			device.default = #{ENV['last_device']}
			device.tooltip = Select the device in the list to which to send the message.
			device.mandatory = true
			b.type = defaultbutton
			b.label = Send
			cb.type = cancelbutton
			cb.label = Cancel
			tx.type = textbox
			tx.label = Pushover notification
			tx.tooltip = You can modify the content of the notification here.
			tx.default = #{data.chomp}
			tx.width = 360
			tx.height = 90
		"
		result = $dz.pashua(pconfig)

		# Device selection canceled by user
		if result['cb'] == '1'
			$dz.fail('Sending canceled.')
		end

		device = result['device']
		puts "Selected device: "+device.to_s

		# Keep last used device
		$dz.save_value('last_device', device)

		# Specify a device for the notification
		if device != send_to_all_title
			notification.device = device
		end

		# Modified message
		if not result['tx'].empty?
			notification.message = result['tx'].gsub("[return]","\n")
		end
	end

	notification.push # send the message

	$dz.finish("Message sent via Pushover")
	$dz.url(false)
end

def dragged
	send($items[0])
end

def select_prefered_website
	pconfig = "
		*.title = Pushover Website
		website.type = popup
		website.option = Pushover Client
		website.option = Pushover Website
		website.label = Choose the Pushover webpage to open by default.
		t.type = text
		t.default = For Pushover Desktop Users you can choose the client website when you click on the action, otherwise select the homepage.
	"
	result = $dz.pashua(pconfig)

	website_choice = if result['website'] == "Pushover Client" then '1' else '0' end
	$dz.save_value('website_choice', website_choice)
	return website_choice
end

def clicked

	# Clicked action open Pushover webpage
	website_choice = ENV['website_choice']

	if website_choice.nil?
		website_choice = select_prefered_website()
	end

	choice = website_choice.to_i
	puts "Open website "+@po_website[choice]
	system("open "+@po_website[choice])

	# update devices
	notification = Notification.new('pushover', ENV['api_key'])
	notification.pushover_devices

end

# require 'net/http'
require 'net/https'
require 'uri'
require 'action.rb'
require 'json'

class Notification

	attr_accessor :service, :title, :link_url, :link_name, :sound, :device

	PO_TOKEN = 'aAAXwYRyTCJr4W7i7JtabmSmtgUf7f'
	BC_ICON = 'https://aptonic.com/dropzone3/images/dz3-icon.jpg'

	def initialize(service, api_key)

		service_title = service.capitalize

		case service
			when 'boxcar'
				url = 'https://new.boxcar.io/api/notifications'
			when 'pushover'
				url = 'https://api.pushover.net/1/messages.json'
			else
				$dz.fail("Unknow service #{service_title}.")
		end

		$dz.fail("Please define your #{service_title} User Api Key!") if api_key == ''

		@service = service
		@url = URI.parse(url)
		@api_key = api_key
		@data = {}
	end

	def compose_data
		if @service == 'boxcar'
			# Define data for Boxcar push notification service
			data = {
				'user_credentials'           => @api_key,
				'notification[title]'        => @title,
				'notification[source_name]'  => "Dropzone 3",
				'notification[long_message]' => @message,
				'notification[sound]'        => @sound,
				'notification[icon_url]'     => BC_ICON
			}
			data['notification[open_url]'] = @link_url if !@link_url.nil?

		elsif @service == 'pushover'
			# Define data for Pushover API
			data = {
				'token'   => PO_TOKEN,
				'user'    => @api_key,
				'message' => @message,
				'sound'   => @sound
			}
			if !@link_url.nil?
				data['url'] = @link_url 
				data['url_title'] = 'Open the link'
			end
			data['device'] = @device if !@device.nil?
		end
		@data = data
	end

	def pushover_devices
		puts 'Request update of User devices from Pushover Services'
		uri = URI.parse("https://api.pushover.net/1/users/validate.json?user=#{@api_key}&token=#{PO_TOKEN}")
		http = Net::HTTP.new(uri.host, uri.port)
		http.read_timeout = 30
		http.use_ssl = true
		http.verify_mode = OpenSSL::SSL::VERIFY_PEER
		request = Net::HTTP::Post.new(uri.request_uri)

		begin
			# {"status":1,"group":0,"devices":["iPad","iPhone","Mac"],"request":"0807658720802"}
			response = http.request(request)
			pushover_response = JSON.parse(response.body);
		rescue StandardError => error
			puts "Http Error: #{error}"
			$dz.error("Pushover Devices", "An error occured when trying to update the devices list from pushover.")
			return nil
		end

		if response.code.to_i == 200 && pushover_response['status'].to_i == 1

			devices = pushover_response['devices'].join(',') if pushover_response['devices'].is_a?(Array)

			if ! devices.nil?
				$dz.save_value('devices', devices)
			end
			devices
		else
			$dz.fail("Something goes wrong on devices update, verify your Internet connection or your User key.")
		end
	end

	def push
		compose_data
		request = Net::HTTP::Post.new(@url.path, initheader = {'Content-Type' =>'application/json'})
		request.set_form_data(@data)
		res = Net::HTTP.new(@url.host, @url.port)
		res.use_ssl = true
		res.verify_mode = OpenSSL::SSL::VERIFY_PEER
		begin
			res.start { |http| 
				response = http.request(request) 
				if response.code.to_i != 200 and response.code.to_i != 201
					service_title = @service.capitalize
					$dz.fail("Please verify your #{service_title} Api Key.")
				end
			}
		rescue StandardError => error
			puts "Http Error: #{error}"
			$dz.fail("An error occured when trying to send your message to #{@service} service.")
			return false
		end
	end

	def message=(message)
		if message.length < 5 || message.nil? || message.empty?
			$dz.fail("Message is empty, nothing to send.")
		end

		url_regx = URI::regexp(['http','https','dav','ftp','ssh','tel'])
		if message =~ url_regx
			puts "Message contains an URL"
			url = message.slice(url_regx)
			url_host = URI.parse(url).host.downcase

			@title = "[Dropzone] Link on #{url_host}"
			@link_url = url
		else
			@title = "[Dropzone] " + message[0,50] + '...'
		end
		@message = message
	end
end
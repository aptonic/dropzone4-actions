require 'lib/faraday'
require 'lib/json'

class Slack
	def initialize
		@slack_api_url = "https://slack.com/"
		@slack_channels_list_url = "/api/channels.list"
		@slack_files_upload_url = "/api/files.upload"
		@slack_post_message_url = "/api/chat.post_message"

		@conn = Faraday.new(:url => @slack_api_url) do |faraday|
			faraday.request  :multipart
			faraday.request  :url_encoded
		  	faraday.response :logger                 
		  	faraday.adapter  Faraday.default_adapter 
		end
	end
	
	def get_channels
		response = @conn.post @slack_channels_list_url, { :token => ENV['api_key'].to_s }

		case response.status
		when 200
		  channels_response = JSON.parse response.body
		else
		  $dz.error("Error", "An error occured while retrieving the list of channels from Slack!")
		end

		if !channels_response['ok']
			$dz.error("Error", channels_response.error)
		end

		channels_response['channels']
	end

	def upload_file (filePath, channel_id)
		fileName = filePath.split(File::SEPARATOR).last
		$dz.begin("Uploading #{fileName} to Slack...")

		contentType = `file -Ib #{filePath}`.gsub(/\n/,"")
		file_upload = Faraday::UploadIO.new(filePath, contentType)

		response = @conn.post @slack_files_upload_url, { :token => ENV['api_key'].to_s, :file => file_upload, :channels => channel_id }
		
		case response.status
		when 200
		  channels_response = JSON.parse response.body
		else
		  $dz.error("Error", "An error occured while uploading the file(s) to Slack!")
		end

		if !channels_response['ok']
			$dz.error("Error", channels_response['error'])
		end
  	end

  	def post_message (message, channel_id)
		escaped_message = escape_message(message)

		response = @conn.post @slack_post_message_url, { :token => ENV['api_key'].to_s, :text => escaped_message, :channels => channel_id }
		
		case response.status
		when 200
		  channels_response = JSON.parse response.body
		else
		  $dz.error("Error", "An error occured while posting the message to Slack!")
		end

		if !channels_response['ok']
			$dz.error("Error", channels_response['error'])
		end
  	end

  	def escape_message(message)
  		message.gsub! '<' '&lt;'
  		message.gsub! '>' '&gt;'
  		message.gsub! '&' '&amp;'
  	end

  	def select_channel
  		channels = get_channels()
	
  		channels_map = {}
		channels.each do |channel|
			channels_map[channel['name']] = channel['id']
  		end
	
  		channel_names = ""
  		channels_map.each_key do |key|
  			channel_names = channel_names + "\"" + key + "\" "
  		end
	
  		output = $dz.cocoa_dialog("dropdown --button1 \"OK\" --button2 \"Cancel\" --title \"Choose channel\" --text \"In which channel would you like to upload the file(s)?\" --items #{channel_names}")
   		button, channel_index = output.split("\n")
  	
   		if button == "2"
   		  $dz.fail("Cancelled")
   		end
	
   		channel_index_int = Integer(channel_index)
   		channel_id = channels_map.values[channel_index_int]

   		channel_id
  	end
end
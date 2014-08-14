require 'lib/faraday'
require 'lib/json'

class Slack
	def initialize
		@slackApiURL = "https://slack.com/"
		@slackChannelsListURL = "/api/channels.list"
		@slackFilesUploadURL = "/api/files.upload"

		@conn = Faraday.new(:url => @slackApiURL) do |faraday|
			faraday.request  :multipart
			faraday.request  :url_encoded
		  	faraday.response :logger                 
		  	faraday.adapter  Faraday.default_adapter 
		end
	end
	
	def getChannels
		response = @conn.post @slackChannelsListURL, { :token => ENV['api_key'].to_s }

		case response.status
		when 200
		  channelsResponse = JSON.parse response.body
		else
		  $dz.error("Error", "An error occured while retrieving the list of channels from Slack!")
		end

		if !channelsResponse['ok']
			$dz.error("Error", channelsResponse.error)
		end

		channelsResponse['channels']
	end

	def uploadFile (filePath, channelId)
		fileName = filePath.split(File::SEPARATOR).last
		$dz.begin("Uploading #{fileName} to Slack...")

		contentType = `file -Ib #{filePath}`.gsub(/\n/,"")
		fileUpload = Faraday::UploadIO.new(filePath, contentType)

		response = @conn.post @slackFilesUploadURL, { :token => ENV['api_key'].to_s, :file => fileUpload, :channels => channelId }
		
		case response.status
		when 200
		  channelsResponse = JSON.parse response.body
		else
		  $dz.error("Error", "An error occured while uploading the file(s) to Slack!")
		end

		if !channelsResponse['ok']
			$dz.error("Error", channelsResponse['error'])
		end
  	end
end
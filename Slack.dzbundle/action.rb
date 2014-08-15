# Dropzone Action Info
# Name: Slack
# Description: Uploads files to a Slack channel
# Handles: Files
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: APIKey
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 1000

require 'lib/faraday'
require 'slack'

def dragged
  	slack = Slack.new

  	$dz.determinate(false)
    
  	$dz.begin("Getting list of channels from Slack...")

  	channel_id = slack.select_channel()
  	# commented this out until I figure out how to post a message to Slack as a user and not as a bot
    # if ENV['dragged_type'] == "files"
    	$items.each do |file|
    		slack.upload_file(file, channel_id)
  		end
	
  		$dz.finish("File(s) were uploaded into Slack!")
    # else
    # 	$items.each do |message|
    # 		slack.post_message(message, channel_id)
  	# 	end
	# 
  	# 	$dz.finish("Message(s) were posted into Slack!")
    # end
    
  	$dz.url(false)
end

def clicked
  	system("open https://www.slack.com/")
end
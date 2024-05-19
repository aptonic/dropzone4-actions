# Dropzone Action Info
# Name: Slack
# Description: Uploads files to a Slack channel \n\nIn order to get the token needed for the API Key field below, login at https://slack.com with your account and afterwards go to https://api.slack.com. Scroll down and copy the token value from the Authentication section in the API Key below.
# Handles: Files
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: APIKey
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.1
# MinDropzoneVersion: 3.0
# UniqueID: 1019

require 'lib/faraday'
require 'slack'

def dragged
  	slack = Slack.new

  	$dz.determinate(false)
    
  	$dz.begin('Getting list of channels from Slack...')

  	channel_id = slack.select_channel
  	# commented this out until I figure out how to post a message to Slack as a user and not as a bot
    # if ENV['dragged_type'] == "files"
    	$items.each do |file|
    		slack.upload_file(file, channel_id)
  		end
	
  		$dz.finish('File(s) were uploaded into Slack!')
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
  	system('open https://www.slack.com/')
end
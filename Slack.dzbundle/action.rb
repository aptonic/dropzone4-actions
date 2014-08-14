# Dropzone Action Info
# Name: Slack
# Description: Uploads files or text to a Slack channel
# Handles: Files, Text
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: APIKey
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.2.1
# RubyPath: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/bin/ruby
# UniqueID: 1000

require 'slack'

def dragged
  	slack = Slack.new

  	$dz.determinate(false)
    
  	$dz.begin("Getting list of channels from Slack...")

  	channels = slack.getChannels()

  	channelsMap = {}
	channels.each do |channel|
		channelsMap[channel['name']] = channel['id']
  	end

  	channelNames = ""
  	channelsMap.each_key do |key|
  		channelNames = channelNames + "\"" + key + "\" "
  	end

  	output = $dz.cocoa_dialog("dropdown --button1 \"OK\" --button2 \"Cancel\" --title \"Choose channel\" --text \"In which channel would you like to upload the file(s)?\" --items #{channelNames}")
    button, channelIndex = output.split("\n")
  
    if button == "2"
      $dz.fail("Cancelled")
    end

    channelIndexInt = Integer(channelIndex)
    channelId = channelsMap.values[channelIndexInt]

    $items.each do |file|
    	slack.uploadFile(file, channelId)
  	end

  	$dz.finish("File(s) were uploaded into the chosen Slack channel!")
  	$dz.url(false)
end

def clicked
  	system("open https://www.slack.com/")
end
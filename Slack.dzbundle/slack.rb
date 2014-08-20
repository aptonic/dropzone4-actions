require 'lib/faraday'
require 'lib/json'

class Slack
  Channel = Struct.new(:channel_name, :channel_id)

  def initialize
    @slack_api_url = 'https://slack.com/'
    @slack_channels_list_url = '/api/channels.list'
    @slack_files_upload_url = '/api/files.upload'
    @slack_post_message_url = '/api/chat.post_message'

    @conn = Faraday.new(:url => @slack_api_url) do |faraday|
      faraday.request :multipart
      faraday.request :url_encoded
      faraday.response :logger
      faraday.adapter Faraday.default_adapter
    end
  end

  def get_channels
    response = @conn.post @slack_channels_list_url, {:token => ENV['api_key'].to_s}

    case response.status
      when 200
        channels_response = JSON.parse response.body
      else
        $dz.error('Error', 'An error occured while retrieving the list of channels from Slack!')
    end

    unless channels_response['ok']
      $dz.error('Error', channels_response.error)
    end

    channels = Array.new
    channels_response['channels'].each do |channel|
      channels << Channel.new(channel['name'], channel['id'])
    end

    channels
  end

  def upload_file (file_path, channel_id)
    file_name = file_path.split(File::SEPARATOR).last
    $dz.begin("Uploading #{file_name} to Slack...")

    content_type = `file -Ib #{file_path}`.gsub(/\n/, "")
    file_upload = Faraday::UploadIO.new(file_path, content_type)

    response = @conn.post @slack_files_upload_url, {:token => ENV['api_key'].to_s, :file => file_upload, :channels => channel_id}

    case response.status
      when 200
        channels_response = JSON.parse response.body
      else
        $dz.error('Error', 'An error occured while uploading the file(s) to Slack!')
    end

    unless channels_response['ok']
      $dz.error('Error', channels_response['error'])
    end
  end

  def post_message (message, channel_id)
    escaped_message = escape_message(message)

    response = @conn.post @slack_post_message_url, {:token => ENV['api_key'].to_s, :text => escaped_message, :channels => channel_id}

    case response.status
      when 200
        channels_response = JSON.parse response.body
      else
        $dz.error('Error', 'An error occured while posting the message to Slack!')
    end

    unless channels_response['ok']
      $dz.error('Error', channels_response['error'])
    end
  end

  def escape_message(message)
    message.gsub! '<' '&lt;'
    message.gsub! '>' '&gt;'
    message.gsub! '&' '&amp;'
  end

  def select_channel
    channels = get_channels

    saved_channel_name = ENV['channel_name']
    index_saved_channel_name = channels.index { |x| x.channel_name == saved_channel_name }
    no_saved_channel = (saved_channel_name.nil? or saved_channel_name.to_s.strip.length == 0 or index_saved_channel_name.nil? )

    channel_names = ''
    # if there's a valid saved channel name, then display it first and reorder array
    unless no_saved_channel
      channel_names = "#{channel_names} \"#{saved_channel_name}\" "
      channels.insert(0, channels.delete_at(index_saved_channel_name))
    end


    channels.each do |channel|
      unless !no_saved_channel and saved_channel_name == channel.channel_name
        channel_names = "#{channel_names} \"#{channel.channel_name}\""
      end
    end

    output = $dz.cocoa_dialog("dropdown --button1 \"OK\" --button2 \"Cancel\" --title \"Choose channel\" --text \"In which channel would you like to upload the file(s)?\" --items #{channel_names}")
    button, channel_index = output.split("\n")

    if button == '2'
      $dz.fail('Cancelled')
    end

    channel_index_int = Integer(channel_index)
    selected_channel = channels[channel_index_int]
    $dz.save_value('channel_name', selected_channel.channel_name)
    channel_id = selected_channel.channel_id
  end
end
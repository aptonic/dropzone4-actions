# Dropzone Action Info
# Name: AutoRemote
# Description: Drag an URL to automatically open it on your Android device with AutoRemote. Hold Command Key to send a file URL. Click to configure and send a message.
# Handles: Text
# Creator: Dominique Da Silva
# URL: https://apps.inspira.io
# Events: Clicked, Dragged
# KeyModifiers: Command
# OptionsNIB: APIKey
# LoginTitle: Device Key
# SkipConfig: No
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.6
# Version: 1.0
# UniqueID: 7004

require 'net/https'
require 'uri'

@debug = true
@autoremoteserver = "autoremotejoaomgcd.appspot.com"

def autoremote(action, data)

  device_key = ENV['api_key']
  res = nil

  if device_key.nil?
    $dz.fail("Device Key not defined!")
  end

  case action
  when 'sendurl'
    message_url = "http://#{@autoremoteserver}/sendintent?intent=#{data[:shared_url]}&key=#{device_key}"
    message_url << "&password=#{data[:password]}"                 if !data[:password].nil? && !data[:password].empty?
    message_url << "&sender=#{data[:sender]}"                     if !data[:sender].nil? && !data[:sender].empty?
    uri = URI(message_url)
    res = Net::HTTP.get_response(uri)
    obfuscate message_url
  when 'sendmessage'
    message_url =  "https://#{@autoremoteserver}/sendmessage?key=#{device_key}"
    message_url << "&message=#{escapeURL(data[:message])}"        if !data[:message].nil?
    message_url << "&password=#{data[:password]}"                 if !data[:password].nil? && !data[:password].empty?
    message_url << "&target=#{data[:target]}"                     if !data[:target].nil? && !data[:target].empty?
    message_url << "&sender=#{data[:sender]}"                     if !data[:sender].nil? && !data[:sender].empty?
    message_url << "&files=#{data[:files]}"                       if !data[:files].nil? && !data[:files].empty?
    message_url << "&ttl=#{data[:ttl]}"                           if !data[:ttl].nil? && !data[:ttl].empty?
    message_url << "&collapseKey=#{data[:group].gsub(' ','%20')}" if !data[:group].nil? && !data[:group].empty?
    uri = URI(message_url)
    res = Net::HTTP.get_response(uri)
    obfuscate message_url
  end

  if !res.nil?
    if res.body.include? "key is invalid"
      $dz.fail("Your key is invalid. Please check your key and try again.")
    end
    dlog res.body
  end
  return res
end


def escapeURL(uri)
  return URI.escape(uri, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"))
end


def prompt(title, message)
  pconfig = "
    *.title = #{title}
    m.type = text
    m.default = #{message}
    bc.type = cancelbutton
    bc.label = No
    ya.type = defaultbutton
    ya.label = Yes
  "
  result = $dz.pashua(pconfig)
  return (result['ya'] == '1')
end


def dlog(message)
  puts message if @debug == true
end


def obfuscate(uri)
  dlog uri.gsub(/key=(\S{0,10})[^&]+&/,"key=\\1...&").gsub(/sender=(\S{0,10})[^&]+&/,"sender=\\1...&")
end


# Prompt the user if a password is set on the device
def checkPassword
    password = ENV['arpwd']
    if ENV['arpwd'].nil?
      if ENV['arnopwd'] || prompt('Device Password', 'Did your device is protected by a password?')
        pwd = $dz.inputbox('Device Password','Please enter the device password') # Prompt for the password
        $dz.save_value('arpwd', pwd)
      else
        $dz.save_value('arnopwd', '1')
      end
    end
    return password
end


def dragged

  shared_url = $items[0]
  modifiers  = ENV['KEY_MODIFIERS']
  url_regx = URI::regexp(['http','https','ftp','ssh','tel','mailto'])

  if shared_url =~ url_regx
    password = checkPassword()
    uri = escapeURL(shared_url)
    if !modifiers.nil? && modifiers.include?('Command')
      $dz.begin("Send File URL on remote device...")
      $dz.determinate(false)
      res = autoremote 'sendmessage', :message => "Fl=:=#{uri}", :files => uri, :password => password, :sender => ENV['arsender']
    else
      $dz.begin("Open URL on remote device...")
      $dz.determinate(false)
      res = autoremote 'sendurl', :shared_url => uri, :password => password, :sender => ENV['arsender']
    end

    # dlog uri
    # dlog res.code       # => '200'
    # dlog res.message    # => 'OK'
    # dlog res.class.name # => 'Net::HTTPOK'
    dlog res.body

  else
    $dz.fail("Not an URL!")
  end

  $dz.finish("Task Complete")
  $dz.url(false)
end

def clicked

    groupsoptions = ""
    argroups = if ENV['argroups'].nil? then Array.new else ENV['argroups'].split(',') end
    argroups.each {|opt|
      groupsoptions << "groups.option = #{opt}\n"
    }

    pconfig = "
        *.title = AutoRemote
        *.floating = 1
        cmd.type = textbox
        cmd.label = Message
        cmd.placeholder = The text you want to send
        cmd.tooltip = Define the AutoRemote message who will be sent to your device (eg. cappucino=:=coffee)
        cmd.width = 310
        cmd.height = 80
        cmd.default = #{ENV['arcmd']}
        isfile.type = checkbox
        isfile.label = File
        isfile.tooltip = Check if your message is a File URL to send to your device.
        isfile.x = 270
        isfile.y = 275
        pwd.type = password
        pwd.label = Password
        pwd.default = #{ENV['arpwd']}
        pwd.width = 240
        spwd.type = checkbox
        spwd.label = Save
        spwd.default = #{if ENV['arpwd'].nil? then 0 else 1 end}
        spwd.x = 250
        spwd.y = 238
        target.type = textfield
        target.placeholder = Target (Optional)
        target.tooltip = Sets the Target on this message
        target.width = 310
        sender.type = textfield
        sender.placeholder = Act as Sender (Optional)
        sender.tooltip = The device that receives this message will reply to this device key when choosing \"Last Sender\" in the devices list)
        sender.default = #{ENV['arsender']}
        sender.width = 310
        ttl.type = textfield
        ttl.placeholder = Validity time in seconds
        ttl.tooltip = Time in seconds AutoRemote will try to deliver the message for before giving up
        ttl.width = 310
        group.type = textfield
        group.placeholder = Group
        group.label = Message Group
        group.tooltip = If the receiving device is unreachable, only one message in a message group will be delivered. Useful you if e.g. leave a device in airplane mode at night and only want to receive the last of the messages that were sent during that time. Leave blank to deliver all messages.
        group.width = 140
        groups.type = popup
        groups.tooltip = AutoRemote Groups history
        groups.width = 160
        groups.x = 150
        groups.y = 46
        groups.option =
        #{groupsoptions}
        groups.default = #{ENV['argroup']}
        bc.type = button
        bc.label = Fermer
        clear.type = button
        clear.label = Reset
        clear.tooltip = Press this button to clear all saved values
        db.type = defaultbutton
        db.label = Send
    "
    ar    = $dz.pashua(pconfig)
    arcmd = ar['cmd']
    files = nil
    dlog ar

    # Save values (if not cancelled by closing the window)
    if !ar.empty?
      # Save Last Message
      $dz.save_value('arcmd', arcmd)
      # Save Sender
      $dz.save_value('arsender', ar['sender'])
      # Save Used Groups
      if !ar['group'].empty?
        argroups.push(ar['group'])
        argroupsvalue = argroups.uniq.sort.join(',')
        $dz.save_value('argroups', argroupsvalue)
        $dz.save_value('argroup', ar['group'])
        dlog argroupsvalue
      end
      # Save Password (checkbox)
      if ar['spwd'] == '1'
        $dz.save_value('arpwd', ar['pwd'])
      else
        $dz.remove_value('arpwd')
      end
    else
      $dz.fail("Configuration canceled!")
    end

    if ar['bc'] == '1' || ar.count == 0
      $dz.finish("Configuration saved!")
      $dz.url(false)
    elsif ar['clear'] == '1'
      if prompt('AutoRemote Settings', 'Are you sure you want to delete all the saved values on Dropzone?')
        $dz.begin("Removing saved values...")
        $dz.determinate(false)
        $dz.remove_value('arcmd')
        $dz.remove_value('argroup')
        $dz.remove_value('argroups')
        $dz.remove_value('arpwd')
        $dz.remove_value('arnopwd')
        $dz.remove_value('arsender')
        $dz.finish("Clear saved AutoRemote values!")
        $dz.url(false)
      end
    else
      # Send the message from the dialog box
      $dz.fail('AutoRemote message is empty, delivery canceled.') if arcmd.empty?

      $dz.begin("Sending message on remote device...")
      $dz.determinate(false)

      # Get the message group if defined
      group = ar['groups']  if !ar['groups'].empty?
      group = ar['group']   if !ar['group'].empty?

      # Send a file URL
      if ar['isfile'] == '1'
        fileURL = escapeURL(arcmd)
        arcmd = "Fl=:=#{fileURL}"
        files = fileURL
      end

      # Send message
      autoremote 'sendmessage', :message => arcmd, :files => files, :target => ar['target'], :sender => ar['sender'], :password => ar['pwd'], :ttl => ar['ttl'], :group => group

      $dz.finish(if files.nil? then "AutoRemote message sent!" else "AutoRemote File URL sent!" end)
      $dz.url(false)

    end

    $dz.url(false)
end

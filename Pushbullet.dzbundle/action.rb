# Dropzone Action Info
# Name: Pushbullet
# Description: Push file to your Pushbullet. Holding `Option` when dropping reopens the device-select dialog.
# Handles: Files
# Events: Dragged
# Creator: BlahGeek
# URL: http://blog.blahgeek.com/dropzone-pushbullet
# OptionsNIB: APIKey
# KeyModifiers: Option
# LoginTitle: API Key (Copy from Pushbullet account setting)
# Version: 1.0
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0

require 'rubygems'
 
def handle_errors(line)
  if line[0..4] == "curl:"
    if line[6..-1] =~ /Couldn't resolve/
      $dz.fail("Please check your network connection")
    else
      $dz.fail(line[6..-1])
    end
  end
end


def curl_it(cmd)

  begin
    require 'json'
  rescue LoadError
    $dz.fail("Gem json not installed")
    Process.exit
  end

  command = "/usr/bin/curl '-#' -u #{ENV['api_key']}: "
  command << cmd
  command << " 2>&1 | tr -u \"\r\" \"\n\""

  last_output = 0
  is_receiving_json = false
  json_output = ""

  IO.popen(command) do |f|
    while line = f.gets
      if line =~ /\{/ or is_receiving_json
        is_receiving_json = true
        json_output << line
      elsif line =~ /%/
        line_split = line.split(" ")
        file_percent_raw = line_split[1]
        if file_percent_raw != nil
          file_percent = file_percent_raw.to_i
          if last_output != file_percent
            $dz.percent(file_percent) 
            $dz.determinate(false) if file_percent == 100
          end
          last_output = file_percent
        end
      else
        handle_errors(line)
      end
    end
  end

  ret = JSON.parse(json_output)
  if ret.has_key?("error")
    $dz.fail(ret["error"]["message"])
    Process.exit
  end
  return ret

end


def select_device

  $dz.determinate(false)
  $dz.begin("Getting device list...")

  ret = curl_it('https://api.pushbullet.com/api/devices')
  items = '--items'
  ret['devices'].each do |device|
    items << " \"#{device['extras']['model']}:#{device['iden']}\" "
  end
  title = 'Pushbullet'
  text = 'Select target device:'
  dialog_output = $dz.cocoa_dialog("standard-dropdown --title #{title} --text #{text} #{items} --string-output")
  button, text = dialog_output.split("\n")
  if text.nil? or button == 'Cancel'
    $dz.finish('Cancelled')
    $dz.url(false)
    Process.exit
  end
  text.split(':')[-1]
end


def dragged


  if ENV["KEY_MODIFIERS"] == "Option" or not ENV.has_key?("device_iden")
    $dz.save_value("device_iden", select_device)
  end

  $dz.determinate(true)
  file_path = $items[0]
  filename = File.basename(file_path)
  file_path = file_path.gsub('"', '\"')
  $dz.begin("Uploading #{filename}...")

  ret = curl_it("-F 'device_iden=#{ENV['device_iden']}' -F type=file -F \"file=@#{file_path}\" https://api.pushbullet.com/api/pushes")

  $dz.finish("Done, URL Copied.")
  $dz.url(ret["file_url"])
end

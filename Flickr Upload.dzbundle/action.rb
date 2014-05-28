# Dropzone Action Info
# Name: Flickr Upload
# Description: Allows images to be uploaded to Flickr. Holding down the option key while dragging copies the direct image URL.
# Handles: Files
# Events: Clicked, Dragged, Authorize, Get_Token
# KeyModifiers: Option, Command
# Creator: Aptonic Software
# URL: http://aptonic.com
# OptionsNIB: FlickrAuth
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 1004

require 'flickr'

def authorize
  Flickr.authorize(ENV['fresh_auth'])
end

def get_token
  Flickr.get_token(ENV['frob_id'])
end
  
def dragged
  urls, photo_ids = Flickr.do_upload($items, ENV['auth_token'], (ENV['KEY_MODIFIERS'] == "Option"))
  
  if urls.length == 1
    finish_text = "URL is now on clipboard"
    url = urls[0].strip
  elsif urls.length > 1
    finish_text = "Upload Complete"
    url = false
  else
    finish_text = "Upload Failed"
    url = false
  end
  
  if photo_ids.length > 1 or (photo_ids.length == 1 and ENV['KEY_MODIFIERS'] == "Command")
    system("open http://www.flickr.com/tools/uploader_edit.gne?ids=#{photo_ids.join(',')}")
  end
  
  $dz.finish(finish_text)
  $dz.url(url)
end

def clicked
  system("open http://www.flickr.com/")
end

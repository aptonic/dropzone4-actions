# Dropzone Action Info
# Name: Renren
# Version: 2.0
# Description: 点击发布人人状态、拖拽上传人人图片。使用前请点击以下链接查看使用说明。
# Handles: Files
# Events: Clicked, Dragged
# Creator: BlahGeek
# URL: http://blog.blahgeek.com/dropzone3-renren
# OptionsNIB: Login
# LoginTitle: API Details (Click the link to see how-to)
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0

require 'rubygems'
require 'uri'

def get_token
  begin
    require 'json'
    require 'rack/oauth2'
  rescue LoadError
    $dz.fail('Gem rack-oauth2 not installed.')
    Process.exit
  end

  Rack::OAuth2::AccessToken::MAC.new(
    :access_token => URI.unescape(ENV.fetch 'username', '-'),
    :mac_key => URI.unescape(ENV.fetch 'password', '-'),
    :mac_algorithm => 'hmac-sha-1'
  )
end

def handle_response(response)
  body = JSON.parse response
  if body.has_key?("error")
    $dz.fail("发布失败：#{body['error']['message']}")
  else
    $dz.finish("发布成功")
  end
  $dz.url(false)
end

def dragged

  file_path = $items[0]
  filename = File.basename(file_path)
  allowed_exts = ["jpg", "jpeg", "gif", "png", "bmp"]
  ext = File.extname(file_path).downcase[1..-1]
  
  if not allowed_exts.include?(ext)
    $dz.fail("只能上传图片哦")
    return
  end

  text = $dz.cocoa_dialog('standard-inputbox --title "上传图片" --e --informative-text "请输入照片描述："')
  button, text = text.split("\n")
  if button == "2"
    $dz.finish("操作已取消")
    $dz.url(false)
    return
  end
  text = '' if text == nil

  token = get_token()

  File.open($items[0]) do |f|
    $dz.determinate(false)
    $dz.begin("正在上传图片...")
    response = token.post 'https://api.renren.com/v2/photo/upload',
                          :file => f,
                          :description => URI.escape(text) # hack
    handle_response response.body
  end

end


def clicked

  text = $dz.cocoa_dialog('standard-inputbox --title "发布状态" --e --informative-text "请输入状态内容："')
  button, text = text.split("\n")
  if text == nil or button == "2"
    $dz.finish("操作已取消")
    $dz.url(false)
    return
  end

  token = get_token()

  $dz.determinate(false)
  $dz.begin("正在发布...")
  response = token.post 'https://api.renren.com/v2/status/put', :content => text
  handle_response response.body
end

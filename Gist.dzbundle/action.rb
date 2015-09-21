# Dropzone Action Info
# Name: Gist
# Version: 1.0
# Description: Sends the dropped text or files to Gist service (http://gist.github.com/) and put the resulting URL on the clipboard.\nGists are private by default, use any modifier key to create a public one.
# Handles: Files, Text
# Creator: Leonardo Fedalto
# URL: https://github.com/Fedalto
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# LoginTitle: GitHub Access Token
# OptionsNIB: APIKey
# SkipValidation: Yes
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0
# RubyPath: /System/Library/Frameworks/Ruby.framework/Versions/2.0/usr/bin/ruby
# UniqueID: 26496555058669647478


require './bundler/setup'
require 'gist'


def public?
  not ENV['KEY_MODIFIERS'].nil?
end

def create_gist gist_args
  begin
    Gist.multi_gist(
      gist_args,
      access_token: ENV['api_key'].strip,
      public: public?,
    )
  rescue RuntimeError => exc
    if exc.message.include? "Net::HTTPUnauthorized"
      $dz.error("Could not create gist.",
        "Please ensure that the API access token is correct " \
        "and has permission to manage your gists.")
    else
      $dz.error("Could not create gist.", exc.message)
    end
  end
end

def gist_text text
  new_gist = create_gist({'gistfile.txt' => text})
  new_gist['html_url']
end

def gist_files files
  gist_arg = {}
  files.each do |file_path|
    if File.directory? file_path
      $dz.error("Could not create gist", "#{file_path} is a directory")
    end
    filename = File.basename file_path
    gist_arg[filename] = File.read file_path
  end

  new_gist = create_gist gist_arg
  new_gist['html_url']
end

def dragged
  $dz.begin("Creating gist...")
  $dz.determinate(false)

  gist_url = case ENV['dragged_type']
    when 'files'
      gist_files $items
    when 'text'
      gist_text $items[0]
  end

  $dz.finish("Gist URL copied to clipboard")
  $dz.url(gist_url)
end

def clicked
  system("open http://gist.github.com/")
  $dz.url(false)
end

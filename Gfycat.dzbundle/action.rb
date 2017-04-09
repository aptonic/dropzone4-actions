# Dropzone Action Info
# Name: Gfycat
# Description: Uploads gif and mp4 files to gfycat
# Handles: Files
# Creator: Guillermo Moreno
# URL: http://gmq.io
# Events: Dragged
# SkipConfig: Yes
# RunsSandboxed: Yes
# Version: 1.2
# MinDropzoneVersion: 3.0
# UniqueID: 631209396312093963120939

require 'curl_uploader'
require 'securerandom'
require 'rest-client'

# https://gfycat.com/api

UPLOAD_URL = "https://gifaffe.s3.amazonaws.com/"
STATUS_URL = "https://upload.gfycat.com/transcode"
URL = "https://gfycat.com"
AWSACCESSKEYID = "AKIAIT4VU4B7G2LQYKZQ"
POLICY = "eyAiZXhwaXJhdGlvbiI6ICIyMDIwLTEyLTAxVDEyOjAwOjAwLjAwMFoiLAogICAgICAgICAgICAiY29uZGl0aW9ucyI6IFsKICAgICAgICAgICAgeyJidWNrZXQiOiAiZ2lmYWZmZSJ9LAogICAgICAgICAgICBbInN0YXJ0cy13aXRoIiwgIiRrZXkiLCAiIl0sCiAgICAgICAgICAgIHsiYWNsIjogInByaXZhdGUifSwKCSAgICB7InN1Y2Nlc3NfYWN0aW9uX3N0YXR1cyI6ICIyMDAifSwKICAgICAgICAgICAgWyJzdGFydHMtd2l0aCIsICIkQ29udGVudC1UeXBlIiwgIiJdLAogICAgICAgICAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogICAgICAgICAgICBdCiAgICAgICAgICB9"
SIGNATURE="mk9t/U/wRN4/uU01mXfeTe2Kcoc="

def dragged
  $dz.fail('Please upload one file at a time.') if $items.length > 1

  random_string = "#{SecureRandom.hex(5)}"

  uploader = CurlUploader.new
  uploader.upload_url = UPLOAD_URL
  uploader.file_field_name = "file"
  uploader.post_vars = {
    :policy => POLICY,
    :AWSAccessKeyId => AWSACCESSKEYID,
    :acl => "private",
    :signature => SIGNATURE,
    :success_action_status => 200,
    :key => random_string,
    "Content-Type" => `file -b --mime-type #{$items[0].gsub(/ /,"\\ ")}`.gsub(/\n/,"")
  }
  uploader.expects_json_output=false
  uploader.output_start_token = '""'
  results = uploader.upload($items)

  gfycat_rest = RestClient.get "#{STATUS_URL}/#{random_string}"
  gfycat_upload = JSON.parse(gfycat_rest.body)
  puts gfycat_upload.inspect
  $dz.fail("#{gfycat_upload['error']}") unless (gfycat_upload['task'] == 'complete')

  $dz.finish('URL copied to clipboard')
  $dz.url("#{URL}/#{gfycat_upload['gfyName']}")
end
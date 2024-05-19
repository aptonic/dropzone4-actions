# Dropzone Action Info
# Name: Short.io
# Description: Shortens URLs using the Short.io service.\n\nGet your API key from:\nhttps://app.short.io/settings/integrations/api-key
# Handles: Text
# Creator: Aptonic
# URL: https://aptonic.com
# OptionsNIB: ShortIO
# Events: Clicked, Dragged
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 4.80.11
# UniqueID: 1039

from urllib.parse import urlparse
import requests
import json
import os

def dragged():
    dz.begin("Shortening URL...")
    dz.determinate(False)

    long_url = items[0]
    parsed_url = urlparse(long_url)

    if not (parsed_url.scheme and parsed_url.netloc):
        dz.fail("Invalid URL")

    shortened_url = shorten_url(long_url)

    dz.finish("URL Shortened")
    dz.url(shortened_url)

def clicked():
    dz.begin("Shortening URL...")
    dz.determinate(False)

    long_url = dz.read_clipboard()

    parsed_url = urlparse(long_url)

    if not (parsed_url.scheme and parsed_url.netloc):
        dz.fail("Invalid URL")

    print(long_url)
    config = """
    *.title = Confirm Shorten URL
    cb.type = cancelbutton
    txt.type = text
    """
    config = config + f"txt.default = Shorten '{long_url}' using Short.io?"

    result = dz.pashua(config)

    if result['cb'] == "1":
        dz.fail("Cancelled")

    dz.begin('Getting shortened URL...')

    shortened_url = shorten_url(long_url)
    dz.finish("URL Shortened")
    dz.url(shortened_url)

def shorten_url(original_url):
    url = "https://api.short.io/links"

    domain = os.environ['domain']
    secret_key = os.environ['api_key']

    data = {
        "domain": domain,
        "originalURL": original_url
    }

    headers = {
        "content-type": "application/json",
        "authorization": secret_key
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    shortened_url = response.json()["shortURL"]

    return shortened_url
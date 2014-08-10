# Dropzone Action Info
# Name: Rackspace Cloud Files
# Description: Upload file to a configured container of your Rackspace Cloud Files account. Click to change the configured container.
# Handles: Files
# Creator: Alexandru Chirițescu
# URL: http://alexchiri.com
# OptionsNIB: UsernameAPIKey
# Events: Dragged, Clicked
# SkipConfig: No
# RunsSandboxed: No
# Version: 1.0
# MinDropzoneVersion: 3.0
# UniqueID: 230

require 'fog'

@client = Fog::Storage.new(
    :provider => 'rackspace',
    :rackspace_username => ENV['username'],
    :rackspace_api_key => ENV['api_key'],
    :rackspace_region => 'ORD'
)

def dragged
	$dz.determinate(false)
    
    # try to get remote container name from saved values
    remoteContainerName = ENV['container']
    
    # if not available, then read it and save it (what's done when clicked)
    if remoteContainerName.to_s.strip.length == 0
        remoteContainerName = setContainer()
    end
    
    remoteContainer = @client.directories.get(remoteContainerName)
    
    urls ||= Array.new
    
    $items.each do |file|
        urls << uploadFile(file, remoteContainer)
    end
    
    $dz.finish("CDN URL of the file(s) is now on clipboard")
    
    if urls.length == 1
        $dz.url("#{urls[0]}")
    elsif urls.length > 1
        $dz.text(urls.join(" "))
    end
    
end

def clicked
    setContainer
end

def setContainer
    output = $dz.cocoa_dialog('standard-inputbox --title "Container name" --e --informative-text "In what container should the files be uploaded to? (will be created if it doesn\'t exist)"')
    
    button, remoteContainerName = output.split("\n")
    
    # fail if no container name is entered
    if remoteContainerName.to_s.strip.length == 0
        $dz.fail("Container name cannot be empty!")
        elsif
        $dz.save_value('container', remoteContainerName)
    end
    
    remoteContainerName
end

def uploadFile (filePath, directory)
    fileName = filePath.split(File::SEPARATOR).last
    file = directory.files.get(fileName)
    localFile = File.open(filePath)
    
    unless file.nil?
        # delete the remote file, if it exists
        file.destroy
        file.save
    end
    
    $dz.begin("Uploading #{File.basename(fileName)} ...")
        file = directory.files.create(
            :key => fileName,
            :body => localFile
    )
                                      
    file.save
                                      
    file.public_url
end

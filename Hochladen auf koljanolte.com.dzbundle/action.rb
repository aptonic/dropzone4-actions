# Dropzone Action Info
# Name: Hochladen auf koljanolte.com
# Description: Dateien per SFTP und veschlüsseltem Namen auf koljanolte.com/temp/ hochladen.
# Handles: Files
# Creator: Kolja Nolte
# URL: https://www.koljanolte.com
# OptionsNIB: ExtendedLogin
# DefaultPort: 22
# Events: Dragged, TestConnection
# KeyModifiers: Option
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.3
# MinDropzoneVersion: 3.0

require '/Users/Kolja/Library/Application Support/Dropzone 3/Actions/Hochladen auf koljanolte.com.dzbundle/sftp_uploader'

$host_info = {:server   => ENV['server'],
              :port     => ENV['port'],
              :username => ENV['username'],
              :password => ENV['password']}

def dragged
    delete_zip = false

    if ENV['KEY_MODIFIERS'] == "Option"
        # Zip up files before uploading
        if $items.length == 1
            # Use directory or file name as zip file name
            dir_name = $items[0].split(File::SEPARATOR)[-1]
            file     = ZipFiles.zip($items, "#{dir_name}.zip")
        else
            file = ZipFiles.zip($items, "files.zip")
        end

        # Remove quotes
        items      = [file[1..-2]]
        delete_zip = true
    else
        # Recursive upload
        items = $items
    end

    print items

    $dz.begin("Starting transfer...")
    $dz.determinate(false)

    remote_paths = SFTPUploader.do_upload(items, ENV['remote_path'], $host_info)
    ZipFiles.delete_zip(items[0]) if delete_zip

    old_file_name = items[0]
    old_file_name = File.basename(old_file_name)
    new_file_name = encode_url(items[0])
    new_file_name = File.basename(new_file_name)
    finish_text   = "Datei \"#{old_file_name}\" wurde als \"#{new_file_name}\" hochgeladen."

    if remote_paths.length == 1
        filename = remote_paths[0].split(File::SEPARATOR)[-1].strip

        if ENV['root_url'] != nil
            slash = (ENV['root_url'][-1, 1] == "/" ? "" : "/")
            url   = ENV['root_url'] + slash + filename
        else
            url = filename
        end
    else
        if remote_paths.length > 1
            finish_text = "Die ausgewählten Dateien wurden erfolgreich hochgeladen."
            url         = false
        else
            finish_text = "Die hochgeladene Datei ist leer."
            url         = false
        end
    end

    $dz.finish(finish_text)
    $dz.url(encode_url(url))
end

def test_connection
    SFTPUploader.test_connection($host_info)
end
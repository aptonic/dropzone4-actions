# Dropzone Action Info
# Name: Install Application
# Description: Drop an application disk image and it will be mounted, installed and ejected. The application will then be launched.
# Handles: Files
# Creator: Aptonic Software
# URL: http://aptonic.com
# Events: Clicked, Dragged
# OptionsNIB: InstallApplication
# Version: 1.3
# RunsSandboxed: No
# MinDropzoneVersion: 3.0
# UniqueID: 1011

require 'installapp'

def dragged
  trash_source = (ENV['trash_source'] ? (ENV['trash_source'] == '1') : true)
  files = "\"#{$items[0]}\""
  destination = InstallApp.install_destination
  app_path = ""
  app_name = ""
  volume_path = ""
  dmg = false
  zip = false
  select_bundle_cancelled = false
  extname = File.extname($items[0]).downcase

  if extname == ".app"
    # Directly copy application
    InstallApp.permissions_check(destination)
    $dz.begin("Copying application...")
    $dz.determinate(true)
    $rsync_copy_extended_attributes = true
    files_copied = Rsync.do_copy($items, destination, false)

    # Trash the .app
    `/bin/mv #{files} ~/.Trash/ >& /dev/null` if files_copied and trash_source

    # Find new app path
    full_source_path = files.split("/")
    app_name = full_source_path[-1][0..-2]
    app_path = "#{destination}#{app_name}"
  elsif extname == ".pkg" or extname == ".mpkg" or extname == ".prefpane"
    InstallApp.open_bundle($items[0])
  elsif extname == ".dmg"
    # Mount DMG, find application inside and copy
    $dz.begin("Attaching disk image...")
    $dz.determinate(false)
    system("xattr -d com.apple.quarantine #{files} >& /dev/null")
  
    # Use DiskImageMounter first if DMG has license agreement or requires authentication
    used_diskimagemounter = false
    agreement_result = `/bin/echo -n | /usr/bin/hdiutil imageinfo -stdinpass #{files} 2>&1 | grep -e "Software License Agreement" -e "Authentication error"`
    if agreement_result =~ /true/ or agreement_result =~ /Authentication error/
      ls_output = `/bin/ls /Volumes/ 2>&1`
      num_volumes_before = ls_output.split("\n").length
      system("open -W -a DiskImageMounter #{files}")
      ls_output = `/bin/ls /Volumes/ 2>&1`
      num_volumes_after = ls_output.split("\n").length
      if num_volumes_before == num_volumes_after
        # Volume can't have mounted
        $dz.finish("Mount Failed")
        $dz.url(false)
        Process.exit
      end
      used_diskimagemounter = true
    end
  
    mount_result = `/usr/bin/hdid #{files} 2>&1`
    if mount_result =~ /hdid:\sattach failed\s/
      $dz.finish("Mount Failed")
      $dz.url(false)
      Process.exit
    end
    
    volume_path = mount_result.split("\n")[-1].split("\t")[-1]
    app_to_install = InstallApp.get_bundle_to_install(volume_path)
    InstallApp.open_bundle(app_to_install)
    app_file = File.basename(app_to_install)
    dmg = true

    if app_to_install != "CANCELLED"
      InstallApp.permissions_check(destination)
      $dz.begin("Copying application...")
      $dz.determinate(true)
      $rsync_copy_extended_attributes = true
      Rsync.do_copy([app_to_install], destination, false)
      app_path = "#{destination}#{app_file}"
    end
    
    actual_vol_name = volume_path.split("/")[-1].gsub(/.app/, "")
    system("osascript eject.scpt \"#{actual_vol_name}\" >& /dev/null") if used_diskimagemounter
    
    if app_to_install == "CANCELLED"
      select_bundle_cancelled = true
      trash_source = false
    end
  elsif extname == ".zip"
    $dz.begin("Unzipping archive...")
    $dz.determinate(false)
    
    if not File.writable?(File.dirname($items[0]))
      $dz.finish("No write permission")
      $dz.url(false)
      Process.exit
    end
    
    system("xattr -d com.apple.quarantine #{files} >& /dev/null")
    
    # Extract, find application inside and copy
    unzip_dir_name = File.dirname($items[0]) + "/" + File.basename($items[0]).split(".")[0]
    unzip_result = `/usr/bin/unzip -o -d \"#{unzip_dir_name}\" #{files} -x __MACOSX/* 2>&1`
    
    app_to_install = InstallApp.get_bundle_to_install(unzip_dir_name)
    InstallApp.open_bundle(app_to_install)
    app_file = File.basename(app_to_install)
    
    if app_to_install != "CANCELLED"      
      InstallApp.permissions_check(destination)
      $dz.begin("Moving application...")  
      $dz.determinate(true)
      $rsync_copy_extended_attributes = true
      Rsync.do_copy([app_to_install], destination, true)
      app_path = "#{destination}#{app_file}"
    end
    
    if app_to_install == "CANCELLED"
      select_bundle_cancelled = true
      trash_source = false
    end
    
    # Delete temporary unzip folder (if empty)
    num_files = Dir.entries(unzip_dir_name).length - 2
    if num_files <= 0
      `/bin/rmdir \"#{unzip_dir_name}\" >& /dev/null`
    else
      system("open \"#{unzip_dir_name}\"")
    end
    
    # Trash the .zip
    `/bin/mv #{files} ~/.Trash/ >& /dev/null` if trash_source
    
    zip = true
  else 
    $dz.finish("Not an Application")
    $dz.url(false)
    Process.exit
  end

  if not select_bundle_cancelled
    # Launch application
    $dz.determinate(false)
    $dz.begin("Launching application...")
    system("xattr -d com.apple.quarantine \"#{app_path}\" >& /dev/null")
    system("open \"#{app_path}\"")
  end

  # Eject disk image if possible
  if not dmg and not zip
    ls_output = `/bin/ls /Volumes/ 2>&1`
    mounted_volumes = ls_output.split("\n")
    app_name_no_ext = app_name.gsub(/.app/, "")
    actual_vol_name = ""

    mounted_volumes.each do |vol| 
      if vol =~ /#{app_name_no_ext}/
        actual_vol_name = vol
        break
      end
    end
    
    volume_path = "/Volumes/#{actual_vol_name}" if actual_vol_name != ""
  end

  if File::exists?(volume_path)
    info = `/usr/bin/hdiutil info`
    $dz.begin("Ejecting disk image...")
    system("osascript eject.scpt \"#{actual_vol_name}\"  >& /dev/null")
    `/usr/bin/hdiutil detach \"/Volumes/#{actual_vol_name}\" >& /dev/null`

    # Move disk image to trash
    if not dmg
      volume_name = "/Volumes/#{actual_vol_name}"
      sections = info.split("================================================")
      dmg_path = ""
      sections.each do |section|
      	if section =~ /\s#{volume_name}\n/
      		dmg_path = section.split("\n")[1].split(":")[1].strip
      		dmg_path = "\"#{dmg_path}\""
      		break
      	end
      end
    else
      dmg_path = files
    end

    `/bin/mv #{dmg_path} ~/.Trash/ >& /dev/null` if trash_source
  end

  if select_bundle_cancelled
    $dz.finish("Cancelled")
    $dz.url(false)
    Process.exit
  end

  $dz.finish("Application Installed")
  $dz.url(false)
end

def clicked
  system("open #{InstallApp.install_destination}")
end

#!/usr/bin/env ruby

require 'find'

# Install Application action helper methods

$SELECT_APP_PATH = "SelectAppDialog.app/Contents/MacOS/SelectAppDialog"

class InstallApp
  
  def self.get_bundle_to_install(dir)
    possible_bundles = []
    package_types = ['.app', '.pkg', '.mpkg', '.prefpane']

    # Search for installable bundles in the given directory
    Find.find(dir) do |path|
      Find.prune if File.basename(path)[0] == ?.
      extname = File.extname(path).downcase
      if package_types.include?(extname)
        possible_bundles << path 
        Find.prune
      end
    end
    
    possible_bundles.sort! {|a, b| a.count("/") <=> b.count("/")}

    if possible_bundles.length < 1
      system("open \"#{dir}\" >& /dev/null")
      $dz.finish("Application not found")
      $dz.url(false)
      Process.exit
    end

    if possible_bundles.length > 1
      files = ""
      possible_bundles[0,8].each { |file| files += "\"#{file}\" "}
      bundle_result = `\"#{$SELECT_APP_PATH}\" #{files} 2>&1`.strip
    else
      bundle_result = possible_bundles[0]
    end
    
    return bundle_result
  end
  
  def self.open_bundle(bundle)
    openable_bundles = ['.pkg', '.mpkg', '.prefpane']
    extname = File.extname(bundle).downcase
    if openable_bundles.include?(extname)
      system("xattr -d com.apple.quarantine \"#{bundle}\" >& /dev/null")
      system("open \"#{bundle}\"")
      $dz.finish("Installer Launched")
      $dz.url(false)
      Process.exit
    end
  end
  
  def self.permissions_check(destination)
    if not File.writable?(destination)
      $dz.error("Cannot copy to Applications folder", "You do not have the needed permissions to copy applications to the main Applications folder.\n\nEither log in as an administrator or create an Applications folder in your user directory and try again.")
    end
  end
  
  def self.install_destination
    # If user has an Applications folder in their home directory then install there
    if File::exists?(File.expand_path("~/Applications")) and ENV['REMOTE_PATH'] != "MAINFOLDER"
      return File.expand_path("~/Applications") + "/"
    else
      return "/Applications/"
    end
  end
  
end
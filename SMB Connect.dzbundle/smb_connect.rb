require 'shellwords'
require 'uri'
require 'fileutils'

class SMBConnect

  # ---------------------------------------------------------------------------
  # Config from ExtendedLogin OptionsNIB
  # ---------------------------------------------------------------------------

  def server
    ENV['server'].to_s.strip.sub(%r{\Asmb://}i, '').sub(%r{\A//}, '').split('/').first.to_s.strip
  end

  def share
    ENV['remote_path'].to_s.strip.sub(%r{\A/+}, '')
  end

  def username; ENV['username'].to_s.strip; end
  def password; ENV['password'].to_s;       end

  # After macOS mounts via open smb://, it lands at /Volumes/<sharename>
  # (or /Volumes/<sharename>-1 etc. if there's a conflict)
  def find_mount_point
    Dir.glob("/Volumes/#{share}*").find { |d| `mount 2>/dev/null`.include?(d) }
  end

  def already_mounted?
    !find_mount_point.nil?
  end

  # ---------------------------------------------------------------------------
  # Public interface
  # ---------------------------------------------------------------------------

  def connect
    validate!
    if already_mounted?
      mpt = find_mount_point
      $dz.begin("Opening #{share}...")
      system("open #{Shellwords.escape(mpt)}")
      $dz.finish("Opened in Finder")
    else
      $dz.begin("Connecting to \\\\#{server}\\#{share}...")
      # Let macOS mount natively — it handles /Volumes creation and Keychain auth
      system("open #{Shellwords.escape(finder_url)}")
      $dz.finish("Connecting via Finder...")
    end
    $dz.url(false)
  rescue => e
    $dz.error("SMB Connect Error", e.message)
  end

  def copy_files(items)
    validate!

    # Mount if needed, then wait up to 10s for macOS to complete it
    unless already_mounted?
      $dz.begin("Mounting #{share}...")
      system("open #{Shellwords.escape(finder_url)}")
      10.times do
        break if already_mounted?
        sleep 1
      end
    end

    mpt = find_mount_point
    unless mpt
      $dz.error("Mount Failed", "Could not mount //#{server}/#{share} within 10 seconds.")
      return
    end

    total  = items.length
    copied = 0
    errors = []
    $dz.begin("Copying #{total} item#{total == 1 ? '' : 's'} to #{share}...")

    items.each_with_index do |src, idx|
      dst = File.join(mpt, File.basename(src))
      begin
        File.directory?(src) ? FileUtils.cp_r(src, dst) : FileUtils.cp(src, dst)
        copied += 1
      rescue => e
        errors << "#{File.basename(src)}: #{e.message}"
      end
      $dz.percent(((idx + 1).to_f / total * 100).round)
    end

    if errors.empty?
      $dz.finish("Copied #{copied} item#{copied == 1 ? '' : 's'} to #{share}")
    else
      $dz.error("Partial Copy", "#{copied}/#{total} copied.\n\nFailed:\n#{errors.join("\n")}")
    end
    $dz.url(false)
  rescue => e
    $dz.error("SMB Connect Error", e.message)
  end

  # ---------------------------------------------------------------------------
  # Private
  # ---------------------------------------------------------------------------

  private

  def validate!
    raise "Server is not configured. Right-click the tile → Settings." if server.empty?
    raise "Share path is not configured. Right-click the tile → Settings." if share.empty?
  end

  def finder_url
    if username.empty?
      "smb://#{server}/#{share}"
    else
      "smb://#{URI.encode_www_form_component(username)}:#{URI.encode_www_form_component(password)}@#{server}/#{share}"
    end
  end

end

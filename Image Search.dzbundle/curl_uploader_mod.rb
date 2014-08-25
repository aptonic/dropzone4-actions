require 'json'

class CurlUploaderMod
  attr_accessor :error_message, :upload_url, :headers, :post_vars, :file_field_name, :expects_json_output, :output_start_token
  
  TRANSLATE_NEWLINES_COMMAND = "2>&1 | tr -u \"\r\" \"\n\""
  
  def initialize
    @file_field_name = "file"
    @output_start_token = '"success"'
    @expects_json_output = true
    @current_path = ""
    @results = []
    @post_vars = {}
    @headers = {}
    @num_files = 0
    @overall_progress = 0
  end

  def upload(file_paths)
    header_string = ""
    @headers.keys.each do |key|
      header_string << "-H \"#{key}: #{@headers[key]}\" "
    end
    header_string.strip!
    
    post_vars_string = ""
    @post_vars.keys.each do |key|
      post_vars_string << "-F \"#{key}=#{@post_vars[key]}\" "
    end
    post_vars_string.strip!
    @num_files = file_paths.length
    
    $dz.determinate(true)
    
    file_paths.each_with_index do |file_path, n|
      @current_path = file_path
      @overall_progress = (100 / @num_files) * n
      launch_curl(file_path, header_string, post_vars_string)
    end
  
    return @results
  end
  
  def launch_curl(file_path, headers, post_vars)
    filename = File.basename(file_path)
    created_symlink = false

    # curl can't handle commas or semicolons in posted file paths, so if the filename has a comma,
    # symlink in temp folder without the disallowed characters and upload that
    if file_path =~ /,|;/
      symlink_path = $dz.temp_folder + "/" + filename.gsub(/,|;/, ' ')
      File.symlink(file_path, symlink_path)
      file_path = symlink_path
      created_symlink = true
    end

    file_path.gsub!('"', '\"')
    file_upload_param = "-F \"#{file_field_name}=@#{file_path}\""
    
    @last_output = 0
    @is_receiving_final_output = false
    @final_output = ""
    @curl_output_valid = false
    
    $dz.begin("Uploading #{filename}...")
    IO.popen("/usr/bin/curl -# #{headers} #{post_vars} #{file_upload_param} \"#{@upload_url}\" #{TRANSLATE_NEWLINES_COMMAND}") do |f|
      while line = f.gets do
        process_line(line)
      end
    end
    
    `rm -f \"#{file_path}\"` if created_symlink
    
    if @curl_output_valid
      if expects_json_output
        begin
          extracted_json = /\{".*\}/.match(@final_output)[0]
          @final_output = JSON.parse(extracted_json)
        rescue
          @curl_output_valid = false
        end
      end
    end

    @results << {:curl_output_valid => @curl_output_valid, :output => @final_output}
  end
  
  def process_line(line)
    if line =~ /%/ and not @is_receiving_final_output
      line_split = line.split(" ")
      file_percent_raw = line_split[1]
      if file_percent_raw != nil
        file_percent = file_percent_raw.to_i
        file_progress = (file_percent / @num_files).to_i
        if @last_output != file_progress
          overall_progress = @overall_progress + file_progress
          $dz.percent(overall_progress)
          $dz.determinate(false) if overall_progress >= 100
        end
        @last_output = file_progress
      end
    end
    if line =~ /#{@output_start_token}/ or @is_receiving_final_output
      @is_receiving_final_output = true
      @final_output += line
      @curl_output_valid = true
    else
      handle_errors(line)
    end
  end
  
  def handle_errors(line)
    if line[0..4] == "curl:"
      @curl_output_valid = false
      curl_message = line[6..-1]
      if curl_message =~ /Couldn't resolve/
        @final_output = "Please check your network connection."
      else
        @final_output = curl_message
      end
    end
  end
  
end

# Dropzone Action Info
# Name:                 Quick image converter and compressor
# Description:          Converts one or more image files into JPG, resizes it to maximum 1000px and compresses it to 75%. A great solution for images intended to be used on websites or blogs.
# Handles:              Files
# Creator:              Kolja Nolte
# URL:                  https://www.koljanolte.com
# Events:               Dragged
# KeyModifiers:         Command, Option, Control, Shift
# SkipConfig:           No
# RunsSandboxed:        Yes
# Version:              1.1.0
# MinDropzoneVersion:   3.0

def dragged
  $dz.determinate(true)

  # Maximum width of compressed images
  max_width = 1000

  # Quality of the output image (0 = worst, 100 = best)
  image_quality = 75

  # Images dragged and dropped into the app
  image_paths = Array $items

  # Now, the actual process starts
  $dz.begin('Begin compressing and resizing images...')

  # Getting the path of the parent directory of the first image
  image_parent_directory_path = File.dirname(image_paths[0])

  # We add this to get a unique MD5 hash
  random_number = rand(99)

  # Initial process percentage
  percent = 0

  # Set initial process percentage
  $dz.percent(percent)

  # Loop to check whether the images exists
  image_paths.each do |image_path|
    next unless File.exist?(image_path)

    # Now, get the MD5 hash of the current image file
    md5_hash = `md5 -q "#{image_path}"` + random_number.to_s

    # Cut it; nobody likes long file names
    md5_hash = md5_hash[1..8]

    # Add the file ending. We know it's jpg because we're going to convert it in the next step
    new_image_file_name = md5_hash + '.jpg'

    # Build the path
    new_image_file_path = image_parent_directory_path + '/' + new_image_file_name

    percent += 100 / image_paths.count

    # Run a couple of shell commands
    `bin/convert '#{image_path}' -quiet -quality #{image_quality} -flatten -resize '#{max_width}x#{max_width}>' '#{new_image_file_path}'`
    `bin/jpegoptim -q --strip-all -o '#{new_image_file_path}'`
    `bin/image_optim --no-pngout --no-svgo '#{new_image_file_path}'`

    # Update process percentage
    $dz.percent(percent)
  end

  # Define notification message
  message        = 'Successfully compressed 1 image.'
  message_plural = "Successfully compressed #{image_paths.count} images."
  message        = message_plural if image_paths.count > 1

  # Display notification message
  $dz.finish(message)

  # Nope, we don't need anything in our clipboard
  $dz.text(false)
end

# THE END
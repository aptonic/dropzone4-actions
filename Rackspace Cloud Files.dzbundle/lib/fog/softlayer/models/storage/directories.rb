#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/collection'
require 'fog/softlayer/models/storage/directory'

module Fog
  module Storage
    class Softlayer

      class Directories < Fog::Collection

        model Fog::Storage::Softlayer::Directory

        def all
          data = service.get_containers.body
          load(data)
        end

        def get(key, options = {})
          data = service.get_container(key, options)
          directory = new(:key => key)
          for key, value in data.headers
            if ['X-Container-Bytes-Used', 'X-Container-Object-Count'].include?(key)
              directory.merge_attributes(key => value)
            end
          end
          directory.files.merge_attributes(options)
          directory.files.instance_variable_set(:@loaded, true)

          data.body.each do |file|
            directory.files << directory.files.new(file)
          end
          directory
        rescue Fog::Storage::Softlayer::NotFound
          nil
        end

      end

    end
  end
end

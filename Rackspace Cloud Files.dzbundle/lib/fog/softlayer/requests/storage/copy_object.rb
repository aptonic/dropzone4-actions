module Fog
  module Storage
    class Softlayer
      class Mock
        def copy_object(source_container, source_object, target_container, target_object, options={})
          response = Excon::Response.new
          if @containers[source_container].nil? || @containers[source_container][source_object].nil? || @containers[target_container].nil?
            response.body = '<html><h1>Not Found</h1><p>The resource could not be found.</p></html>'
            response.status = 404
          else # Success
            @containers[target_container][target_object] = @containers[source_container][source_object]
            response.body = ''
            response.status = 201
          end
          response
        end
      end

      class Real

        # Copy object
        #
        # ==== Parameters
        # * source_container_name<~String> - Name of source bucket
        # * source_object_name<~String> - Name of source object
        # * target_container_name<~String> - Name of bucket to create copy in
        # * target_object_name<~String> - Name for new copy of object
        # * options<~Hash> - Additional headers
        def copy_object(source_container, source_object, target_container, target_object, options={})
          headers = { 'X-Copy-From' => "/#{source_container}/#{source_object}" }.merge(options)
          request({
            :expects  => 201,
            :headers  => headers,
            :method   => 'PUT',
            :path     => "#{Fog::Softlayer.escape(target_container)}/#{Fog::Softlayer.escape(target_object)}"
          })
        end

      end
    end
  end
end

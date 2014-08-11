module Fog
  module Storage
    class Softlayer
      class Mock

        def delete_object(container, object)
          response = Excon::Response.new
          if @containers[container].nil? || @containers[container][object].nil? # Container or object doesn't exist.
            response.body = '<html><h1>Not Found</h1><p>The resource could not be found.</p></html>'
            response.status = 404
          else # Success
            response.body = ''
            response.status = 204
          end
          response
        end

      end


      class Real

        # Delete an existing object
        #
        # ==== Parameters
        # * container<~String> - Name of container to delete
        # * object<~String> - Name of object to delete
        #
        def delete_object(container, object)
          request(
            :expects  => 204,
            :method   => 'DELETE',
            :path     => "#{Fog::Softlayer.escape(container)}/#{Fog::Softlayer.escape(object)}"
          )
        end

      end
    end
  end
end

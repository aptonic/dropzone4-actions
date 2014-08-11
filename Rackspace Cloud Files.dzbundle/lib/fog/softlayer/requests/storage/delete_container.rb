module Fog
  module Storage
    class Softlayer
      class Mock
        def delete_container(name)
          response = Excon::Response.new
          if @containers[name].nil? # Container doesn't exist.
            response.body = '<html><h1>Not Found</h1><p>The resource could not be found.</p></html>'
            response.status = 404
          elsif @containers[name].length > 0  # Container not empty
            response.body = '<html><h1>Conflict</h1><p>There was a conflict when trying to complete your request.</p></html>'
            response.status = 409
          else # Success
            response.body = ''
            response.status = 204
          end
          response
        end
      end

      class Real
        # Delete an existing container
        #
        # ==== Parameters
        # * name<~String> - Name of container to delete
        #
        def delete_container(name)
          request(
            :expects  => 204,
            :method   => 'DELETE',
            :path     => Fog::Softlayer.escape(name)
          )
        end

      end
    end
  end
end

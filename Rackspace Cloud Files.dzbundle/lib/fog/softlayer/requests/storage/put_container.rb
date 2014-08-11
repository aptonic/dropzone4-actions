module Fog
  module Storage
    class Softlayer
      class Mock
        def put_container(name)
          @containers[name] = {} unless @containers[name]
          response = Excon::Response.new
          response.body = ''
          response.status = 201
          response
        end
      end

      class Real

        # Create a new container
        #
        # ==== Parameters
        # * name<~String> - Name for container, should be < 256 bytes and must not contain '/'
        #
        def put_container(name)
          request(
            :expects  => [201, 202],
            :method   => 'PUT',
            :path     => Fog::Softlayer.escape(name)
          )
        end

      end
    end
  end
end

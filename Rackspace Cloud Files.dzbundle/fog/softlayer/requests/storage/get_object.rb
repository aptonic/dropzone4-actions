module Fog
  module Storage
    class Softlayer
      class Mock
        def get_object(container, object, &block)
          if @containers[container] && @containers[container][object]
            response = Excon::Response.new
            response.body = @containers[container][object]
            response.status = 200
            response
          else
            response = Excon::Response.new
            response.body = '<html><h1>Not Found</h1><p>The resource could not be found.</p></html>'
            response.status = 404
            response.headers = {"Content-Length"=>"70", "Content-Type"=>"text/html; charset=UTF-8", "X-Trans-Id"=>"abcdefghijklmnopqrstuvwx-0123456789", "Date"=>Time.now}
            response
          end
        end
      end
      class Real

        # Get details for object
        #
        # ==== Parameters
        # * container<~String> - Name of container to look in
        # * object<~String> - Name of object to look for
        #
        def get_object(container, object, &block)
          params = {
            :expects  => 200,
            :method   => 'GET',
            :path     => "#{Fog::Softlayer.escape(container)}/#{Fog::Softlayer.escape(object)}"
          }

          if block_given?
            params[:response_block] = block
          end

          request(params, false)
        end

      end
    end
  end
end

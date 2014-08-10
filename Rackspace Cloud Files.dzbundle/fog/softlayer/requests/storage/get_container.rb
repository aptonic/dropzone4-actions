module Fog
  module Storage
    class Softlayer
      class Mock
        def get_container(container, options = {})
          if @containers[container]
            response = Excon::Response.new
            response.body = @containers[container].map do |name, object|
              {
                  'hash' => object.respond_to?(:to_s) ? Digest::MD5.hexdigest(object.to_s) : 'e4d909c290d0fb1ca068ffaddf22cbd0',
                  'last_modified' => Time.now,
                  'bytes' => Memory.analyze(container).bytes,
                  'content/type' => 'application/json'
              }
            end
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

        # Get details for container and total bytes stored
        #
        # ==== Parameters
        # * container<~String> - Name of container to retrieve info for
        # * options<~String>:
        #   * 'limit'<~String> - Maximum number of objects to return
        #   * 'marker'<~String> - Only return objects whose name is greater than marker
        #   * 'prefix'<~String> - Limits results to those starting with prefix
        #   * 'path'<~String> - Return objects nested in the pseudo path
        #
        # ==== Returns
        # * response<~Excon::Response>:
        #   * headers<~Hash>:
        #     * 'X-Account-Container-Count'<~String> - Count of containers
        #     * 'X-Account-Bytes-Used'<~String> - Bytes used
        #   * body<~Array>:
        #     * 'bytes'<~Integer> - Number of bytes used by container
        #     * 'count'<~Integer> - Number of items in container
        #     * 'name'<~String> - Name of container
        #     * item<~Hash>:
        #       * 'bytes'<~String> - Size of object
        #       * 'content_type'<~String> Content-Type of object
        #       * 'hash'<~String> - Hash of object (etag?)
        #       * 'last_modified'<~String> - Last modified timestamp
        #       * 'name'<~String> - Name of object
        def get_container(container, options = {})
          options = options.reject {|key, value| value.nil?}
          request(
            :expects  => 200,
            :method   => 'GET',
            :path     => Fog::Softlayer.escape(container),
            :query    => {'format' => 'json'}.merge!(options)
          )
        end

      end
    end
  end
end

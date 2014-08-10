module Fog
  module Storage
    class Softlayer
      class Mock
        def get_containers(options = {})
          response = Excon::Response.new
          response.body = _format_containers(@containers)
          response.status = 200
          response
        end

        private

        def _format_containers(containers)
          containers.map do |name, container|
            meta = Memory.analyze(container)
            {'count' => container.length, 'bytes' => meta.bytes, 'name' => name}
          end
        end
      end

      class Real

        # List existing storage containers
        #
        # ==== Parameters
        # * options<~Hash>:
        #   * 'limit'<~Integer> - Upper limit to number of results returned
        #   * 'marker'<~String> - Only return objects with name greater than this value
        #
        # ==== Returns
        # * response<~Excon::Response>:
        #   * body<~Array>:
        #     * container<~Hash>:
        #       * 'bytes'<~Integer>: - Number of bytes used by container
        #       * 'count'<~Integer>: - Number of items in container
        #       * 'name'<~String>: - Name of container
        def get_containers(options = {})
          options = options.reject {|key, value| value.nil?}
          request(
            :expects  => [200, 204],
            :method   => 'GET',
            :path     => '',
            :query    => {'format' => 'json'}.merge!(options)
          )
        end

      end
    end
  end
end

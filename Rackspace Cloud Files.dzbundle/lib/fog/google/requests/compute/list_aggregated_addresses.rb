module Fog
  module Compute
    class Google
      class Mock
        def list_aggregated_addresses(options = {})
          Fog::Mock.not_implemented
        end
      end

      class Real
        def list_aggregated_addresses(options = {})
          api_method = @compute.addresses.aggregated_list
          parameters = {
            'project' => @project,
          }
          parameters['filter'] = options[:filter] if options[:filter]

          result = self.build_result(api_method, parameters)
          response = self.build_response(result)
        end
      end
    end
  end
end

module Fog
  module Compute
    class Google
      class Mock
        def get_disk_type(identity, zone)
          disk_types = list_disk_types(zone).body['items']
          disk_type = disk_types.select { |dt| dt['name'] == identity } || []
          if disk_type.empty?
            return build_response(:body => {
              'error' => {
                'errors' => [
                  {
                    'domain' => 'global',
                    'reason' => 'notFound',
                    'message' => "The resource 'projects/#{@project}/zones/#{zone}/diskTypes/#{identity}' was not found",
                  }
                ],
                'code' => 404,
                'message' => "The resource 'projects/#{@project}/zones/#{zone}/diskTypes/#{identity}' was not found",
              }
            })
          end

          build_response(:body => disk_type.first)
        end
      end

      class Real
        def get_disk_type(identity, zone)
          api_method = @compute.disk_types.get
          parameters = {
            'project'  => @project,
            'zone'     => zone.split('/')[-1],
            'diskType' => identity,
          }

          result = self.build_result(api_method, parameters)
          response = self.build_response(result)
        end
      end
    end
  end
end

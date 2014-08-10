#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
module Fog
  module Compute
    class Softlayer

      class Mock
        def get_bare_metal_server(identifier)
          response = Excon::Response.new
          response.body = @bare_metal_servers.map {|vm| vm if vm['id'] == identifier.to_s }.compact.first || {}
          response.status = response.body.empty? ? 404 : 200
          if response.status == 404
            response.body = {
                "error"=>"Unable to find object with id of '#{identifier}'.",
                "code"=>"SoftLayer_Exception_ObjectNotFound"
            }
          end
          response
        end

      end

      class Real
        def get_bare_metal_server(identifier)
          request(:hardware_server, identifier, :expected => [200, 404], :query => 'objectMask=mask[datacenter,tagReferences,memory,provisionDate,processorCoreAmount,hardDrives,datacenter,hourlyBillingFlag,operatingSystem.softwareLicense.softwareDescription.referenceCode,sshKeys.id,privateNetworkOnlyFlag]')
        end
      end
    end
  end
end

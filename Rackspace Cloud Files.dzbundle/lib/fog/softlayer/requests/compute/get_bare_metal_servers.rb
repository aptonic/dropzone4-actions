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
        def get_bare_metal_servers
          response = Excon::Response.new
          response.body = @bare_metal_servers
          response.status = 200
          response
        end

      end

      class Real
        def get_bare_metal_servers
          request(:account, :get_hardware, :query => 'objectMask=mask[datacenter,tagReferences,memory,processorCoreAmount,hardDrives,datacenter,hourlyBillingFlag,operatingSystem.softwareLicense.softwareDescription.referenceCode,sshKeys.id,privateNetworkOnlyFlag]')
        end
      end
    end
  end
end

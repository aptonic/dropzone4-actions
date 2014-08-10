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
        def get_vms
          response = Excon::Response.new
          response.body = @virtual_guests
          response.status = 200
          response
        end

      end

      class Real
        def get_vms
          request(:account, :get_virtual_guests, :query => 'objectMask=mask[datacenter,tagReferences,blockDevices,blockDeviceTemplateGroup.globalIdentifier,operatingSystem.softwareLicense.softwareDescription.referenceCode,primaryNetworkComponent.networkVlan,sshKeys.id,privateNetworkOnlyFlag]')
        end
      end
    end
  end
end

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
        def get_vm(identifier)
          response = Excon::Response.new
          response.body = @virtual_guests.map {|vm| vm if vm['id'] == identifier.to_s }.compact.first || {}
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
        def get_vm(identifier)
          request(:virtual_guest, identifier, :expected => [200, 404], :query => 'objectMask=mask[datacenter,tagReferences,blockDevices,blockDeviceTemplateGroup.globalIdentifier,operatingSystem.softwareLicense.softwareDescription.referenceCode,sshKeys.id,privateNetworkOnlyFlag]')
        end
      end
    end
  end
end

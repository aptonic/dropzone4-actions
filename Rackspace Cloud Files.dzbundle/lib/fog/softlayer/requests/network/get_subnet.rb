#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

module Fog
  module Network
    class Softlayer

      class Mock

        def get_subnet(id)
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def get_subnet(id)
          self.request(:network_subnet, "#{id}/get_object", :query => 'objectMask=mask[datacenter,ipAddresses.id,virtualGuests.fullyQualifiedDomainName,virtualGuests.id,hardware.fullyQualifiedDomainName,hardware.id]')
        end
      end
    end
  end
end

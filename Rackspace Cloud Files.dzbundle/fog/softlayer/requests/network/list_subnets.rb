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

        def list_subnets
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def list_subnets
        self.request(:account, :get_subnets, :query => 'objectMask=mask[networkVlan,ipAddresses.id,datacenter,hardware,virtualGuests.id,virtualGuests.fullyQualifiedDomainName]')
        end
      end
    end
  end
end

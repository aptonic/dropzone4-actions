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

        def get_ip_addresses
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def get_ip_addresses
          self.request(:account, :get_ip_addresses, :query => 'objectMask=mask[hardware.fullyQualifiedDomainName,hardware.id,virtualGuest.id,virtualGuest.fullyQualifiedDomainName,subnet.id]')
        end
      end
    end
  end
end

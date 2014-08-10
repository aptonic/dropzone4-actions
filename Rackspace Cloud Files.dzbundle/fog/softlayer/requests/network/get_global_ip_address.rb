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

        def get_global_ip_address(id)
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def get_global_ip_address(id)
          self.request(:network_subnet_ipaddress_global, id, :query => 'objectMask=mask[ipAddress,destinationIpAddress]')
        end
      end
    end
  end
end

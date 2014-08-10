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

        def unroute_global_ip(global_ip_id)
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def unroute_global_ip(global_ip_id)
          self.request(:network_subnet_ipaddress_global, "#{global_ip_id}/unroute")
        end
      end
    end
  end
end

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

        def delete_global_ip_address(id)
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def delete_global_ip_address(id)
          billing = self.request(:network_subnet_ipaddress_global, "#{id}/get_billing_item").body
          billing.nil? and raise "Global IP Address with ID #{id} not found."
          request(:billing_item, "#{billing['id']}/cancel_service")
        end
      end
    end
  end
end

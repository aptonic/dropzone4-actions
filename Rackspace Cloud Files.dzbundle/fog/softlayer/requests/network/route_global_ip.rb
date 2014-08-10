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

        def route_global_ip(global_ip, destination_ip)
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def route_global_ip(global_ip_id, destination_ip_address)
          self.request(:network_subnet_ipaddress_global, "#{global_ip_id}/route", :body => destination_ip_address, :http_method => :post)
        end
      end
    end
  end
end

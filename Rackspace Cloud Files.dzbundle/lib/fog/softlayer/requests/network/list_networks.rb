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

        def list_networks
          response = Excon::Response.new
          response.body = @networks
          response.status = 200
          response
        end

      end

      class Real
        def list_networks
          self.request(:account, :get_network_vlans, :query => 'objectMask=mask[subnets.id,subnets.note,subnets.subnetType,type,primaryRouter.datacenter,tagReferences,networkSpace]')
        end
      end
    end
  end
end

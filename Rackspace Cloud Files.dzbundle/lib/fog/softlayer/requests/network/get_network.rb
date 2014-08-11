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

        def get_network(id)
          response = Excon::Response.new
          response.status = 200
          response.body = @networks.select { |vlan| vlan['id'] == id }.first
          if response.body.nil?
            response.status = 404
            response.body = "{\"error\":\"Unable to find object with id of '#{id}'.\",\"code\":\"SoftLayer_Exception_ObjectNotFound\"}"
          end
          response
        end

      end

      class Real
        def get_network(id)
          self.request(:network_vlan, "#{id}/get_object", :query => 'objectMask=mask[subnets,tagReferences,type,primaryRouter.datacenter,networkSpace]')
        end
      end
    end
  end
end

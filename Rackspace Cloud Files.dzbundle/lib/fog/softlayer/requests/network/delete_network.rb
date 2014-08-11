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

        def delete_network(id)
          response = Excon::Response.new
          response.status = 200
          if @networks.reject! { |vlan| vlan['id'] == id }.nil?
            response.status = 404
            response.body = "{\"error\":\"Unable to find object with id of '#{id}'.\",\"code\":\"SoftLayer_Exception_ObjectNotFound\"}"
          else
            response.body = true
          end
          response
        end

      end

      class Real
        def delete_network(id)
          billing_id = request(:network_vlan, "#{id}/get_billing_item").body['id']
          billing_id.nil? and raise "SoftLayer VLAN with ID #{id} cannot be deleted." # will be automatically deleted when hardware using it is deleted.
          request(:billing_item, "#{billing_id}/cancel_service").body
        end
      end
    end
  end
end

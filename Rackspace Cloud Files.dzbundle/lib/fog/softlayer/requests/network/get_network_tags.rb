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

        def get_network_tags(id)
          response = Excon::Response.new

          response.status = self.get_network(id).status

          net = self.get_network(id).body
          unless net['error']
            tags = @tags.map do |tag|
              tag if tag['resourceTableId'] == id
            end.compact
          end

          net['tagReferences'] = tags if net.is_a?(Hash)
          response.body = net

          if response.status == 404
            response.body = {
                "error"=>"Unable to find object with id of '#{id}'.",
                "code"=>"SoftLayer_Exception_ObjectNotFound"
            }
          end
          response
        end

      end

      class Real
        def get_network_tags(id)
          self.request(:network_vlan, id, :query => 'objectMask=mask[tagReferences]')
        end
      end
    end
  end
end

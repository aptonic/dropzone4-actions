#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

module Fog
  module Compute
    class Softlayer

      class Mock

        def get_bare_metal_tags(id)
          response = Excon::Response.new

          response.status = self.get_bare_metal_server(id).status

          bmc = self.get_bare_metal_server(id).body
          unless bmc['error']
            tags = @tags.map do |tag|
              tag if tag['resourceTableId'] == id
            end.compact
          end

          bmc['tagReferences'] = tags
          response.body = bmc

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
        def get_bare_metal_tags(id)
          self.request(:hardware_server, id, :query => 'objectMask=id;tagReferences')
        end
      end
    end
  end
end

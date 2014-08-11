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

        def get_vm_tags(id)
          response = Excon::Response.new

          response.status = self.get_vm(id).status

          vm = self.get_vm(id).body
          unless vm['error']
            tags = @tags.map do |tag|
              tag if tag['resourceTableId'] == id
            end.compact
          end

          vm['tagReferences'] = tags
          response.body = vm

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
        def get_vm_tags(id)
          self.request(:virtual_guest, id, :query => 'objectMask=mask[tagReferences]')
        end
      end
    end
  end
end

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

        def delete_vm_tags(id, tags = [])
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          response = Excon::Response.new
          response.status = self.get_vm(id).status

          if response.status != 404
            @tags = @tags.reject do |tag|
              tag['resourceTableId'] == id and tags.include?(tag['tag']['name'])
            end
            response.body = true
          else
            response.body = {
                "error"=>"Unable to find object with id of '#{id}'.",
                "code"=>"SoftLayer_Exception_ObjectNotFound"
            }
          end
          response
        end

      end

      class Real
        def delete_vm_tags(id, tags = [])
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          subset = self.get_vm_tags(id).body['tagReferences'].map do |i|
            i['tag']['name'] unless tags.include?(i['tag']['name'])
          end.compact
          self.create_vm_tags(id, subset)
        end
      end
    end
  end
end

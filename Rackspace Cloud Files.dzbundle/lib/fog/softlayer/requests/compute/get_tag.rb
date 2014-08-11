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

        def get_tag(id)
          # TODO: Implement
        end

      end

      class Real
        def get_tag(id)
          self.request(:tag, "#{id}/get_object", :query => "objectMask=references;references.tagType")
        end
      end
    end
  end
end

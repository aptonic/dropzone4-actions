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

        def describe_tags
          response = Excon::Response.new
          response.body = @tags
          response.status = 200
          response
        end

      end

      class Real
        def describe_tags
          self.request(:account, :get_tags, :query => 'objectMask=mask[referenceCount]')
        end
      end
    end
  end
end

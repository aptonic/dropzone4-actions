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
        def get_key_pairs
          response = Excon::Response.new
          response.body = @key_pairs
          response.status = 200
          response
        end

      end

      class Real
        def get_key_pairs
          request(:account, :get_ssh_keys)
        end
      end
    end
  end
end

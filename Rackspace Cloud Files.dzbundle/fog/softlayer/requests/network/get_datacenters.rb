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

        def get_datacenters
          response = Excon::Response.new
          response.status = 200
          response.body = @datacenters
          response
        end

      end

      class Real
        def get_datacenters
          request(:location_datacenter, :get_datacenters)
        end
      end
    end
  end
end

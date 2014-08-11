#
# Author:: Celso Fernandes (<fernandes@zertico.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
module Fog
  module DNS
    class Softlayer

      class Mock
        def get_domains
          response = Excon::Response.new
          response.body = @softlayer_domains
          response.status = 200
          return response
        end

      end

      class Real
        def get_domains
          request(:account, :get_domains)
        end
      end
    end
  end
end

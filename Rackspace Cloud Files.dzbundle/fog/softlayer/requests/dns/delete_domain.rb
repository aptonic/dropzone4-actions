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
        def delete_domain(id)
          @softlayer_domains.each do |domain|
            if domain[:id].to_i == id
              @softlayer_domains.delete(domain)
              response = Excon::Response.new
              response.body = true
              response.status = 200
              return response
            end
          end
          raise Excon::Errors::NotFound
        end

      end

      class Real
        def delete_domain(id)
          request(:dns_domain, id.to_s, :http_method => :DELETE)
        end
      end
    end
  end
end

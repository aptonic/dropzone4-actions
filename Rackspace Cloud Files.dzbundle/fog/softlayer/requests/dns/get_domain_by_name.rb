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
        def get_domain_by_name(name)
          @softlayer_domains.each do |domain|
            if domain[:name] == name
              response = Excon::Response.new
              response.body = [ domain ]
              response.status = 200
              return response
            end
          end
          response = Excon::Response.new
          response.body = [ ]
          response.status = 200
          return response
        end

      end

      class Real
        def get_domain_by_name(name)
          request(:dns_domain, "getByDomainName/" + URI::encode(name.to_s, "-"))
        end
      end
    end
  end
end

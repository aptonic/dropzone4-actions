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
        def get_records(domain_id)
          @softlayer_domains.each do |domain|
            if domain[:id].to_i == domain_id
              response = Excon::Response.new
              response.body = domain[:resourceRecords]
              response.status = 200
              return response
            end
          end
          raise Excon::Errors::NotFound
        end

      end

      class Real
        def get_records(domain_id)
          request(:dns_domain, domain_id.to_s + '/getResourceRecords')
        end
      end
    end
  end
end

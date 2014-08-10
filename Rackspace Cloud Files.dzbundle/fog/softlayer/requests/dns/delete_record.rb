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
        def delete_record(id)
          # Get the domain
          @domain = @softlayer_domains.each do |domain|
            domain[:resourceRecords].each do |record|
              if record["id"] == id
                domain[:serial] = domain[:serial] + 1
                domain[:resourceRecords].delete(record)
              end
            end
          end
          
          response = Excon::Response.new
          response.body = true
          response.status = 200
          response
        end

      end

      class Real
        def delete_record(id)
          request(:dns_domain_resourceRecord, id.to_s, :http_method => :DELETE)
        end
      end
    end
  end
end

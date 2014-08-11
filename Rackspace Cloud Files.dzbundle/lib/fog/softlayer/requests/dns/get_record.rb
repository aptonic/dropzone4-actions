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
        def get_record(id)
          # Get the record
          @softlayer_domains.each do |domain|
            domain[:resourceRecords].each do |record|
              if record["id"].to_i == id.to_i
                response = Excon::Response.new
                response.body = record
                response.status = 200
                return response
              end  
            end
          end
          
          raise Excon::Errors::NotFound
        end

      end

      class Real
        def get_record(id)
          request(:dns_domain_resourceRecord, id)
        end
      end
    end
  end
end

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
        def update_record(record_id, opts)
          
          # Get the domain
          @domain = @softlayer_domains.each do |domain|
            if domain[:id].to_i == opts[:domainId]
              domain
            end
          end
          
          # Get the record
          @domain.first[:resourceRecords].each do |record|
            if record["id"].to_i == record_id.to_i
              @domain.first[:serial] = (@domain.first[:serial] + 1)
              @record = record
            end  
          end
          
          # Update the data
          # ps: Separated the update to make easier future refator
          @record["data"] = opts[:data]
          @record["host"] = opts[:host]
          @record["type"] = opts[:type]
          
          response = Excon::Response.new
          response.body = @domain
          response.status = 200
          return response
        end
      end

      class Real
        def update_record(record_id, opts)
          request(:dns_domain_resourceRecord, record_id, :body => opts, :http_method => :PUT)
        end
      end
    end
  end
end

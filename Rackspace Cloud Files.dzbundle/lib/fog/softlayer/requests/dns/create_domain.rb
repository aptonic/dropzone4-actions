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
        def create_domain(opts)
          response = Excon::Response.new
          updated_at = Time.now
          domain_id = Fog::Mock.random_numbers(7)
          body = {
            :id => domain_id,
            :name => opts["name"],
            :serial => updated_at.strftime("%Y%m%d")+"00",
            :updated_at => updated_at,
            :resourceRecords => [
              {
                "data"=>"ns1."+opts["name"]+".",
                "domainId"=>domain_id,
                "expire"=>604800,
                "host"=>"@",
                "id"=>Fog::Mock.random_numbers(8),
                "minimum"=>3600,
                "mxPriority"=>nil,
                "refresh"=>3600,
                "responsiblePerson"=>"admin."+opts["name"]+".",
                "retry"=>300,
                "ttl"=>86400,
                "type"=>"SOA",
              },
              {
                "data"=>"ns1.softlayer.com.",
                "domainId"=>domain_id,
                "expire"=>nil,
                "host"=>"@",
                "id"=>Fog::Mock.random_numbers(8),
                "minimum"=>nil,
                "mxPriority"=>nil,
                "refresh"=>nil,
                "retry"=>nil,
                "ttl"=>86400,
                "type"=>"NS",
              },
              {
                "data"=>"ns2.softlayer.com.",
                "domainId"=>domain_id,
                "expire"=>nil,
                "host"=>"@",
                "id"=>Fog::Mock.random_numbers(8),
                "minimum"=>nil,
                "mxPriority"=>nil,
                "refresh"=>nil,
                "retry"=>nil,
                "ttl"=>86400,
                "type"=>"NS",
              }
            ]
          }
          response.body = body
          @softlayer_domains << body
          response.status = 200
          response
        end

      end

      class Real
        def create_domain(opts)
          request(:dns_domain, :create_object, :body => opts, :http_method => :POST)
        end
      end
    end
  end
end

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
        def create_record(opts)
          new_record = {
            "id"                => Fog::Mock.random_numbers(8),
            "data"              => opts[:data],
            "domainId"          => opts[:domainId],
            "host"              => opts[:host],
            "type"              => opts[:type],
            "minimum"           => nil,
            "expire"            => nil,
            "mxPriority"        => nil,
            "refresh"           => nil,
            "responsiblePerson" => nil,
            "retry"             => nil,
            "ttl"               => nil,
          }
          @softlayer_domains.each do |domain|
            if domain[:id].to_i == opts[:domainId]
              domain[:serial] = domain[:serial].to_i + 1
              domain[:resourceRecords] << new_record
              response = Excon::Response.new
              response.body = new_record
              response.status = 200
              return response
            end
          end
          raise Excon::Errors::NotFound
        end

      end

      class Real
        def create_record(opts)
          request(:dns_domain_resourceRecord, :create_object, :body => opts, :http_method => :POST)
        end
      end
    end
  end
end

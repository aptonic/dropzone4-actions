#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
module Fog
  module Compute
    class Softlayer

      class Mock

        def create_key_pair(opts)
          response = Excon::Response.new

          response.status = 200
          response.body = []

          response.body = {
              "createDate" => Time.now.iso8601,
              "fingerprint" => "1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a:1a",
              "id" => Fog::Mock.random_numbers(5).to_i,
              "key" => opts[:key],
              "label" => opts[:label],
              "modifyDate" => nil
          }

          @key_pairs.push(response.body)
          response
        end
      end

      class Real
        def create_key_pair(opts)
          request(:security_ssh_key, :create_object, :body => opts, :http_method => :post)
        end
      end

    end
  end
end

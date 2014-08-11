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

        def update_key_pair(id, opts)
          response = Excon::Response.new
          response.status = 200

          key_pair, index = @key_pairs.each_with_index.map { |kp, i| [kp, i] if kp['id'] == id }.compact.flatten

          if key_pair.nil?
            response.status = 404
            response.body = {
                "error" => "Unable to find object with id of '#{id}'.",
                "code" => "SoftLayer_Exception_ObjectNotFound"
            }
          else

            @key_pairs[index] = key_pair.merge(opts)
            response.body = true
          end
          response
        end
      end

      class Real
        def update_key_pair(id, opts)
          request(:security_ssh_key, id, :body => opts, :http_method => :put)
        end
      end

    end
  end
end


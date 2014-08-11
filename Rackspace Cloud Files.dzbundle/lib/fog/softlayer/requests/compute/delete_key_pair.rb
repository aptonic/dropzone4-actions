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

        def delete_key_pair(id)
          response = Excon::Response.new
          response.status = 200
          if @key_pairs.reject! { |kp| kp['id'] == id }.nil?
            response.status = 404
            response.body = {
              "error" => "Unable to find object with id of '#{id}'.",
              "code" => "SoftLayer_Exception_ObjectNotFound"
            }
          else
            response.body = true
          end
          response
        end
      end

      class Real
        def delete_key_pair(id)
          request(:security_ssh_key, id, :http_method => :delete)
        end
      end

    end
  end
end

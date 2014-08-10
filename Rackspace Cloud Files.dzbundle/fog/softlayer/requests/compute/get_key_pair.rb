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
        def get_key_pair(id)
          response = Excon::Response.new
          response.status = 200
          response.body = key_pair = @key_pairs.select { |kp| kp['id'] == id }.first

          if key_pair.nil?
            response.body = {
                "error"=>"Unable to find object with id of '#{id}'.",
                "code"=>"SoftLayer_Exception_ObjectNotFound"
            }
            response.status = 404
          end
          response
        end

      end

      class Real
        def get_key_pair(id)
          request(:security_ssh_key, id)
        end
      end
    end
  end
end

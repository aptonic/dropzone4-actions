#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

module Fog
  module Network
    class Softlayer

      class Mock

        def get_global_ip_records
          # TODO: Implement.
          raise Fog::Errors::MockNotImplemented
        end

      end

      class Real
        def get_global_ip_records
          self.request(:account, :get_global_ip_records)
        end
      end
    end
  end
end

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

        def get_subnet_package_id
          42
        end

      end

      class Real
        def get_subnet_package_id
          request(:product_package, '0/get_configuration', :query => 'objectMask=mask[isRequired,itemCategory]').body.map do |item|
            item['itemCategory']['id'] if item['itemCategory']['categoryCode'] == 'static_sec_ip_addresses'
          end.compact.first
        end
      end
    end
  end
end

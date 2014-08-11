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

        def get_public_vlan_price_code
          42
        end

      end

      class Real
        def get_public_vlan_price_code
          request(:product_package, '0/get_items').body.map { |item| item['prices'][0]['id'] if item['description'] =~ /vlan/i and item['description'] =~ /public/i }.compact.first
        end
      end
    end
  end
end

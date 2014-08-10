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

        def get_subnet_price_code
          42
        end

      end

      class Real
        def get_subnet_price_code
          subnet_package_id = get_subnet_package_id
          request(:product_package, '0/get_item_prices', :query => 'objectMask=mask[id,categories.id,item.description]').body.map do |item|
            item['id'] if item['categories'][0]['id'] == subnet_package_id
          end.compact.first
        end
      end
    end
  end
end

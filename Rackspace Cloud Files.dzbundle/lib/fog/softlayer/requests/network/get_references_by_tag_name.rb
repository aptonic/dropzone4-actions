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

        def get_references_by_tag_name(tag_list)
          response = Excon::Response.new
          response.status = 200

          response.body = tag_list.split(',').map do |tag|
            refs = @tags.select { |ref| ref['tag']['name'] == tag }
            unless refs.empty?
              {
                  'accountId' =>  Fog::Softlayer.mock_account_id,
                  'id'=>Fog::Mock.random_numbers(7),
                  'internal' => 0,
                  'name' => tag,
                  'references' => refs
              }
            end
          end.compact
          response
        end

      end

      class Real
        def get_references_by_tag_name(tag_list)
          self.request(:tag, "get_tag_by_tag_name/#{tag_list}", :query => 'objectMask=references')
        end
      end
    end
  end
end

#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/model'

module Fog
  module Compute
    class Softlayer
      class KeyPair < Fog::Model
        identity :id

        attribute :label
        attribute :create_date,               :aliases => 'createDate'
        attribute :modify_date,               :aliases => 'modifyDate'
        attribute :note,                      :aliases => 'notes'
        attribute :key

        def save
          identity ? update : create
        end

        def create
          requires :key, :label
          response = service.create_key_pair(attributes).body
          merge_attributes(response)
          self
        end

        def update
          requires :id
          merge_attributes(service.update_key_pair(self.id, self.attributes).body)
          self
        end

        def destroy
          requires :id
          service.delete_key_pair(self.id)
          true
        end

      end
    end
  end
end

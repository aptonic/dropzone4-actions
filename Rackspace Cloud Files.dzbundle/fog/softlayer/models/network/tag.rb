#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/model'

module Fog
  module Network
    class Softlayer
      class Tag < Fog::Model
        identity  :id

        attribute :name
        attribute :referenceCount, :type => :integer
        attribute :resource_id
        attribute :internal, :type => :boolean

        def initialize(attributes = {})
          super
        end

        def destroy
          requires :name, :resource_id
          service.delete_network_tags(self.resource_id, [self.name])
          #load_network
          #@network.delete_tags([self.name])
          true
        end

        def references
          @networks ||= service.request(:tag, "#{id}", :query => "objectMask=references;references.tagType").body['references'].map do |ref|
            service.networks.get(ref['resourceTableId']) if ref['tagType']['keyName'] == 'NETWORK_VLAN'
          end.compact
        end

        def save
          requires :name, :resource_id
          load_network
          service.create_network_tags(self.resource_id, @network.tags << self.name)
          true
        end

        private

        def load_network
          requires :resource_id
          @network ||= service.networks.get(self.resource_id)
        end
      end
    end
  end
end

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
          load_server
          @server.bare_metal? ? destroy_bare_metal_tag : destroy_vm_tag
          true
        end

        def references
          @servers ||= service.request(:tag, "#{id}", :query => "objectMask=references;references.tagType").body['references'].map do |ref|
            type = ref['tagType']['keyName']
            service.servers.get(ref['resourceTableId']) if type == 'GUEST' || type == 'HARDWARE'
          end.compact
        end

        def save
          requires :name, :resource_id
          load_server
          @server.bare_metal? ? add_bare_metal_tag : add_vm_tag
          true
        end

        private

        def add_bare_metal_tag
          service.create_bare_metal_tags(@server.id, @server.tags << self.name)
        end

        def add_vm_tag
          service.create_vm_tags(@server.id, @server.tags << self.name)
        end

        def destroy_bare_metal_tag
          service.delete_bare_metal_tags(@server.id, [self.name])
        end

        def destroy_vm_tag
          service.delete_vm_tags(@server.id, [self.name])
        end

        def load_server
          requires :resource_id
          @server ||= service.servers.get(self.resource_id)
        end
      end
    end
  end
end

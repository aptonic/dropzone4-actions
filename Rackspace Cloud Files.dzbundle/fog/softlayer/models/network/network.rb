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
      class Network < Fog::Model
        identity :id

        attribute :name
        attribute :modify_date,               :aliases => 'modifyDate'
        attribute :note
        attribute :tags,                      :aliases => 'tagReferences'
        attribute :type,                      :squash => :keyName
        attribute :datacenter
        attribute :network_space,             :aliases => 'networkSpace'
        attribute :router,                    :aliases => 'primaryRouter'
        #attribute :subnets

        def add_tags(tags)
          requires :id
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          tags.each do |tag|
            service.tags.new(:resource_id => self.id, :name => tag).save
          end
          self.reload
          true
        end

        def datacenter
          @datacenter ||= attributes[:datacenter] or (service.datacenters.new(attributes[:router]['datacenter']) if attributes[:router] and attributes[:router]['datacenter'])
        end

        def delete_tags(tags)
          requires :id
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          tags.each do |tag|
            service.tags.new(:resource_id => self.id, :name => tag).destroy
          end
          self.reload
          true
        end

        def router=(new_data)
          raise ArgumentError, "Network Router must be a Hash." unless new_data.is_a?(Hash)
          attributes[:router] = new_data.select { |k,v| ['id', 'hostname', 'datacenter'].include?(k) }
        end

        def private?
          requires :network_space
          network_space == 'PRIVATE'
        end

        def public?
          requires :network_space
          network_space == 'PUBLIC'
        end

        def save
          identity ? update : create
        end

        def subnets
          requires :id
          @subnets ||= attributes['subnets'].map do |subnet|
            service.subnets.get(subnet['id'])
          end
        end

        def create
          requires :datacenter, :router, :network_space
          response = service.create_network(build_order).body
          merge_attributes(response)
          self
        end

        def update
          requires :id
          merge_attributes(service.update_network(self.id, self.attributes).body)
          self
        end

        def destroy
          requires :id
          service.delete_network(self.id)
          true
        end

        def tags
          requires :id
          attributes[:tags].map { |i| i['tag']['name'] } if attributes[:tags]
        end

        private

        def build_order
          {
              'complexType' => 'SoftLayer_Container_Product_Order_Network_Vlan',
              'name' => name,
              'routerId' =>router['id'],
              'router' => router['hostname'],
              'location' => datacenter.id,
              'quantity' =>1,
              'packageId' =>0,
              'prices' =>[
                  {'id' => public? ? service.get_public_vlan_price_code : service.get_private_vlan_price_code },
                  {'id' => service.get_subnet_price_code }
              ]
          }
        end

      end
    end
  end
end

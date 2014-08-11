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
      class Subnet < Fog::Model
        identity :id

        attribute :name,                  :aliases => 'note'
        attribute :network_id,            :aliases => 'networkIdentifier'
        attribute :vlan_id,               :aliases => 'networkVlanId'
        attribute :cidr
        attribute :ip_version,            :aliases => 'version'
        attribute :type,                  :aliases => 'subnetType'
        attribute :gateway_ip,            :aliases => 'gateway'
        attribute :broadcast,             :aliases => 'broadcastAddress'
        attribute :gateway
        attribute :datacenter,            :squash => :name

        def addresses
          @addresses ||= attributes['ipAddresses'].map do |address|
            service.ips.get(address['id'])
          end
        end

        def save
          requires :network_id, :cidr, :ip_version
          identity ? update : create
        end

        def create
          requires :network_id, :cidr, :ip_version
          merge_attributes(service.create_subnet(self.network_id,
                                                 self.cidr,
                                                 self.ip_version,
                                                 self.attributes).body['subnet'])
          self
        end

        def update
          requires :id, :network_id, :cidr, :ip_version
          merge_attributes(service.update_subnet(self.id,
                                                 self.attributes).body['subnet'])
          self
        end

        def destroy
          requires :id
          service.delete_subnet(self.id)
          true
        end
      end
    end
  end
end

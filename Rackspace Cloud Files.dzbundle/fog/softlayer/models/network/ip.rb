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
      class Ip < Fog::Model
        identity :id

        attribute :subnet_id,            :aliases => 'subnetId'
        attribute :address,              :aliases => 'ipAddress'
        attribute :broadcast,            :aliases => 'isBroadcast'
        attribute :gateway,              :aliases => 'isGateway'
        attribute :network,              :aliases => 'isNetwork'
        attribute :reserved,             :aliases => 'isReserved'
        attribute :global_id
        attribute :destination_ip,       :aliases => 'destinationIpAddress'
        attribute :note
        attribute :assigned_to,           :aliases => ['hardware', 'virtualGuest']

        def initialize(attributes)
          @connection = attributes[:connection]
          super
        end

        def save
          requires :subnet_id
          identity ? update : create
        end

        def create

        end

        def update
          self
        end

        def destination_ip=(ip)
          if ip.is_a?(Hash)
            attributes[:destination_ip] = Fog::Network::Softlayer::Ip.new(ip)
          elsif ip.is_a?(Fog::Network::Softlayer::Ip) or ip.nil?
            attributes[:destination_ip] = ip
          else
            raise ArgumentError, "Invalid argument type in #{self.class.name}##{__method__}."
          end
        end

        def destroy
          raise "Only Global IP Addresses can be destroyed.  Regular IP Addresses are part of Fog::Softlayer::Network::Subnet" unless global?
          service.delete_global_ip_address(self.global_id).status == 200
        end

        def broadcast?
          !!attributes[:broadcast]
        end

        def gateway?
          !!attributes[:gateway]
        end

        def global?
          !!attributes[:global_id]
        end

        def network?
          !!attributes[:network]
        end

        def reserved?
          !!attributes[:reserved]
        end

        def route(dest_ip)
          requires :global_id
          raise ArgumentError, "Invalid argument type in #{self.class.name}##{__method__}." unless dest_ip.is_a?(Fog::Network::Softlayer::Ip)
          raise ArgumentError, "The destination IP may not be the network address of the destination subnet" if dest_ip.network?
          raise ArgumentError, "The destination IP may not be the gateway address of the destination subnet" if dest_ip.gateway?
          raise ArgumentError, "The destination IP may not be the broadcast address of the destination subnet" if dest_ip.broadcast?
          raise ArgumentError, "The destination IP may not be another global IP address" if dest_ip.global?
          service.route_global_ip(self.global_id, dest_ip.address).status == 200
        end

        def routed?
          !!self.assigned_to or !!self.destination_ip
        end

        def unroute
          requires :global_id
          service.unroute_global_ip(self.global_id).status == 200
        end

      end
    end
  end
end

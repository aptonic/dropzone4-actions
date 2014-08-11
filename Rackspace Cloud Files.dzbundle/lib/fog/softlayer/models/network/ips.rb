#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/collection'
require 'fog/softlayer/models/network/ip'

module Fog
  module Network
    class Softlayer
      class Ips < Fog::Collection
        attribute :filters

        model Fog::Network::Softlayer::Ip

        def initialize(attributes)
          self.filters ||= {}
          super
        end

        def all(filters = filters)
          self.filters = filters
          ips = service.get_ip_addresses.body

          ips.each_with_index do |ip,i|
            if global_records.keys.include?(ip['id'])
              ips[i] = parse_global_ip_record(service.get_global_ip_address(global_records[ip['id']]['id']).body)
            end
          end

          load(ips)
        end

        def by_address(address)
          ip = service.get_ip_addresses.body.select do |ip|
            ip['ipAddress'] == address
          end.first
          new(ip) if ip
        end

        def get(id)
          if global_records.keys.include?(id)
            response = service.get_global_ip_address(global_records[id]['id']).body
            ip = parse_global_ip_record(response)
          else
            ip = service.get_ip_address(id).body
          end

          new(ip) if ip

        rescue Fog::Network::Softlayer::NotFound
          nil
        end

        def global_records
          @records ||= {}
          service.get_global_ip_records.body.each { |record| @records[record['ipAddressId']] = record } if @records.empty?
          @records
        end

        private

        def parse_global_ip_record(record)
          response = service.request(:network_subnet_ipaddress_global, record['id'], :query => 'objectMask=mask[ipAddress,destinationIpAddress]').body
          parsed = response['ipAddress']
          parsed['destinationIpAddress'] = response['destinationIpAddress']
          parsed[:global_id] = record['id']
          parsed
        end
      end
    end
  end
end

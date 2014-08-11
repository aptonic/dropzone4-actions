#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/collection'
require 'fog/softlayer/models/network/network'

module Fog
  module Network
    class Softlayer
      class Networks < Fog::Collection
        model Fog::Network::Softlayer::Network

        def all
          data = service.list_networks.body
          load(data)
        end

        def get(id)
          if network = service.get_network(id).body
            new(network)
          end
        rescue Fog::Network::Softlayer::NotFound
          nil
        end

        def tagged_with(tags)
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          ids = service.get_references_by_tag_name(tags.join(',')).body.map do |tag|
            tag['references'].map do |ref|
              ref['resourceTableId']
            end
          end.flatten.uniq
          ids.map { |id| get(id) }
        end

        def by_name(name)
          all.select { |vlan| vlan.name == name }.first
        end

      end
    end
  end
end

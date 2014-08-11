#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/collection'
require 'fog/softlayer/models/network/datacenter'

module Fog
  module Network
    class Softlayer
      class Datacenters < Fog::Collection
        attribute :filters

        model Fog::Network::Softlayer::Datacenter

        def initialize(attributes)
          self.filters ||= {}
          super
        end

        def all(filters = filters)
          self.filters = filters
          load(service.get_datacenters.body)
        end

        def get(id)
          data = service.request(:location_datacenter, "#{id}/get_object").body
            new.merge_attributes(data)
        rescue Fog::Network::Softlayer::NotFound
          nil
        end

        def by_name(name)
          all.map { |dc| dc if dc.name == name }.compact.first
        end
      end
    end
  end
end

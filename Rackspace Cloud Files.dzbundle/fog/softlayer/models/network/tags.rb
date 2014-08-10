#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/collection'
require 'fog/softlayer/models/network/tag'

module Fog
  module Network
    class Softlayer
      class Tags < Fog::Collection
        attribute :filters

        model Fog::Network::Softlayer::Tag

        def initialize(attributes)
          self.filters ||= []
          super
        end

        def all(filters = filters)
          raise ArgumentError, "Filters argument for #{self.class.name}##{__method__} must be Array." unless filters.is_a?(Array)
          self.filters = filters
          data = service.request(:account, :get_tags, :query => 'objectMask=mask[referenceCount]').body
          data.select! { |tag| filters.include?(tag) } unless filters.empty?
          load(data)
        end

        def get(id)
          return nil if id.nil? || id == ""
          response = service.request(:tag, id)
          data = response.body
          new.merge_attributes(data)
        end
      end
    end
  end
end

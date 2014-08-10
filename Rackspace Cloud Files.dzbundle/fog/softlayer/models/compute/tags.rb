#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/core/collection'
require 'fog/softlayer/models/compute/tag'

module Fog
  module Compute
    class Softlayer
      class Tags < Fog::Collection
        attribute :filters

        model Fog::Compute::Softlayer::Tag

        def initialize(attributes)
          self.filters ||= []
          super
        end

        def all(filters = filters)
          raise ArgumentError, "Filters argument for #{self.class.name}##{__method__} must be Array." unless filters.is_a?(Array)
          self.filters = filters
          data = service.describe_tags.body
          data.select! { |tag| filters.include?(tag) } unless filters.empty?
          load(data)
        end

        def get(id)
          return nil if id.nil? || id == ""
          response = service.get_tag(id)
          data = response.body
          new.merge_attributes(data)
        end
      end
    end
  end
end

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
      class Datacenter < Fog::Model
        identity :id

        attribute :long_name,   :aliases => 'longName'
        attribute :name

        def initialize(attributes)
          @connection = attributes[:connection]
          super
        end

        def routers
          requires :id
          @routers ||= service.get_datacenter_routers(id).body
        end

        def routable_subnets
          requires :id
          @routable_subnets ||= service.request(:location_datacenter, "#{id}/get_bound_subnets").body
        end

        def save
          raise "Not possible."
        end

        def create
          raise "Not possible."
        end

        def update
          raise "Not possible."
        end

        def destroy
          raise "Not possible."
        end
      end
    end
  end
end

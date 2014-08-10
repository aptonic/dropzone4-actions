#
# Author:: Celso Fernandes (<fernandes@zertico.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/collection'
require 'fog/softlayer/models/dns/record'

module Fog
  module DNS
    class Softlayer
      class Records < Fog::Collection
        attribute :domain

        model Fog::DNS::Softlayer::Record

        def all
          requires :domain
          clear
          data = service.get_records(domain.id).body
          load(data)
        end
        
        def get(identifier)
          return nil if identifier.nil? || identifier == ""
          response = service.get_record(identifier)
          data = response.body
          new.merge_attributes(data)
        rescue Excon::Errors::NotFound
          nil
        end

        def new(attributes = {})
          super({ :domain => domain }.merge!(attributes))
        end
      end
    end
  end
end
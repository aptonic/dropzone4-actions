#
# Author:: Celso Fernandes (<fernandes@zertico.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/collection'
require 'fog/softlayer/models/compute/server'

module Fog
  module DNS
    class Softlayer

      class Domains < Fog::Collection

        model Fog::DNS::Softlayer::Domain

        def all
          data = service.get_domains.body
          load(data)
        end

        def get(identifier)
          return nil if identifier.nil? || identifier == ""
          response = service.get_domain(identifier)
          data = response.body
          new.merge_attributes(data)
        rescue Excon::Errors::NotFound
          nil
        end
        
        def get_by_name(name)
          return nil if name.nil? || name == ""
          response = service.get_domain_by_name(name)
          data = response.body
          return false if data.empty?
          new.merge_attributes(data.first)
        rescue Excon::Errors::NotFound
          nil
        end
        
        
        def create(name)
          template_object = {
            'name' => name,
            'resourceRecords' => {},
          }
          response = service.create_domain(template_object)
          data = response.body
          new.merge_attributes(data)
        end

      end

    end
  end
end

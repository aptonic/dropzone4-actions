#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/softlayer/core'
require 'fog/softlayer/compute/shared'

module Fog
  module Compute
    class Softlayer < Fog::Service
      class MissingRequiredParameter < Fog::Errors::Error; end

      # Client credentials
      requires :softlayer_username, :softlayer_api_key

      # Excon connection settings
      recognizes :softlayer_api_url, :softlayer_default_domain, :softlayer_default_datacenter


      model_path 'fog/softlayer/models/compute'
      collection    :flavors
      model         :flavor
      collection    :images
      model         :image
      collection    :key_pairs
      model         :key_pair
      collection    :servers
      model         :server
      collection    :tags
      model         :tag

      request_path 'fog/softlayer/requests/compute'
      request :create_bare_metal_server
      request :create_bare_metal_tags
      request :create_key_pair
      request :create_vm
      request :create_vms
      request :create_vm_tags
      request :delete_bare_metal_server
      request :delete_bare_metal_tags
      request :delete_key_pair
      request :delete_vm
      request :delete_vm_tags
      request :describe_tags
      request :get_bare_metal_server
      request :get_bare_metal_servers
      request :get_bare_metal_tags
      request :get_key_pair
      request :get_key_pairs
      request :get_references_by_tag_name
      request :get_tag
      request :get_vm_tags
      request :get_vm
      request :get_vms
      request :update_key_pair

      # The Mock Service allows you to run a fake instance of the Service
      # which makes no real connections.
      #
      #
      class Mock
        include Fog::Softlayer::Slapi
        include Fog::Softlayer::Compute::Shared
        attr_accessor :default_domain, :virtual_guests, :bare_metal_servers, :softlayer_default_domain, :softlayer_default_datacenter

        def initialize(args)
          @virtual_guests = []
          @bare_metal_servers = []
          @tags = []
          @key_pairs = []
          super(args)
        end

        def request(method, path, options = {})
          _request
        end

        def request_access_token(connection, credentials)
          _request
        end

        def _request
          raise Fog::Errors::MockNotImplemented
        end

        def list_servers
          vms = self.get_vms.body
          bare_metals = self.get_bare_metal_servers.body
          vms.map! { |server| server['bare_metal'] = false }
          bare_metals.map! { |server| server['bare_metal'] = true }
          (vms << bare_metals).flatten
        end

      end

      ##
      # Makes real connections to Softlayer.
      #
      class Real
        attr_accessor :softlayer_default_domain
        attr_accessor :softlayer_default_datacenter
        include Fog::Softlayer::Slapi
        include Fog::Softlayer::Compute::Shared

        def initialize(options={})
          @softlayer_api_key = options[:softlayer_api_key]
          @softlayer_username = options[:softlayer_username]
          @softlayer_default_domain = options[:softlayer_default_domain]
          @softlayer_default_datacenter = options[:softlayer_default_datacenter]
        end

        def request(service, path, options = {})
          options = {:username => @softlayer_username, :api_key => @softlayer_api_key}.merge(options)
          Fog::Softlayer::Slapi.slapi_request(service, path, options)
        end

        def list_servers
          (self.get_vms.body.map {|s| s['bare_metal'] = false; s } << self.get_bare_metal_servers.body.map {|s| s['bare_metal'] = true; s}).flatten
        end


      end

    end

  end
end

## some helpers for some dirty work
class String
  def softlayer_camelize
    self.split('_').inject([]){ |buffer,e| buffer.push(buffer.empty? ? e : e.capitalize) }.join
  end

  def softlayer_underscore
    self.gsub(/::/, '/').
        gsub(/([A-Z]+)([A-Z][a-z])/,'\1_\2').
        gsub(/([a-z\d])([A-Z])/,'\1_\2').
        tr("-", "_").
        downcase
  end
end

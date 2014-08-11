#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/softlayer/core'

module Fog
  module Network
    class Softlayer < Fog::Service

      requires :softlayer_username, :softlayer_api_key


      ## MODELS
      #
      model_path 'fog/softlayer/models/network'
      model       :datacenter
      collection  :datacenters
      model       :network
      collection  :networks
      #model       :port
      #collection  :ports
      model       :subnet
      collection  :subnets
      model       :ip
      collection  :ips
      model       :tag
      collection  :tags
      #model       :router
      #collection  :routers


      ## REQUESTS
      #
      request_path 'fog/softlayer/requests/network'

      request :list_networks
      request :create_network
      request :delete_network
      request :get_network

      request :get_private_vlan_price_code
      request :get_public_vlan_price_code
      request :get_subnet_package_id
      request :get_subnet_price_code
      request :get_datacenters
      request :get_datacenter_routers
      request :get_references_by_tag_name


      request :create_network_tags
      request :delete_network_tags
      request :get_network_tags

      request :list_subnets
      request :get_subnet

      request :get_ip_address
      request :get_global_ip_address
      request :get_ip_addresses
      request :get_global_ip_records
      request :route_global_ip
      request :unroute_global_ip
      request :delete_global_ip_address

      class Mock
        #Fog::Mock.random_ip,

        def self.reset
          @data = nil
        end

        def initialize(options={})
          @softlayer_api_key = options[:softlayer_api_key]
          @softlayer_username = options[:softlayer_username]

          @networks = []
          @datacenters = [
              {"id"=>265592, "longName"=>"Amsterdam 1", "name"=>"ams01"},
              {"id"=>358698, "longName"=>"Ashburn, VA 3", "name"=>"wdc03"},
              {"id"=>3, "longName"=>"Dallas 1", "name"=>"dal01"},
              {"id"=>154770, "longName"=>"Dallas 2", "name"=>"dal02"},
              {"id"=>167092, "longName"=>"Dallas 4", "name"=>"dal04"},
              {"id"=>138124, "longName"=>"Dallas 5", "name"=>"dal05"},
              {"id"=>154820, "longName"=>"Dallas 6", "name"=>"dal06"},
              {"id"=>142776, "longName"=>"Dallas 7", "name"=>"dal07"},
              {"id"=>352494, "longName"=>"Hong Kong 2", "name"=>"hkg02"},
              {"id"=>142775, "longName"=>"Houston 2", "name"=>"hou02"},
              {"id"=>358694, "longName"=>"London 2", "name"=>"lon02"},
              {"id"=>168642, "longName"=>"San Jose 1", "name"=>"sjc01"},
              {"id"=>18171, "longName"=>"Seattle", "name"=>"sea01"},
              {"id"=>224092, "longName"=>"Singapore 1", "name"=>"sng01"},
              {"id"=>448994, "longName"=>"Toronto 1", "name"=>"tor01"},
              {"id"=>37473, "longName"=>"Washington, DC 1", "name"=>"wdc01"}
          ]
          @tags = []
        end

        def credentials
          { :provider           => 'softlayer',
            :softlayer_username => @softlayer_username,
            :softlayer_api_key  => @softlayer_api_key
          }
        end
      end

      class Real
        include Fog::Softlayer::Slapi

        def initialize(options={})
          @softlayer_api_key = options[:softlayer_api_key]
          @softlayer_username = options[:softlayer_username]
        end

        def request(service, path, options = {})
          options = {:username => @softlayer_username, :api_key => @softlayer_api_key}.merge(options)
          Fog::Softlayer::Slapi.slapi_request(service, path, options)
        end

        def create_new_global_ipv4
          order = {
              "complexType" => 'SoftLayer_Container_Product_Order_Network_Subnet',
              "packageId" => 0, # everything that's not a Server is package 0 when using placeOrder
              "prices" => [{"id"=>global_ipv4_price_code}],
              "quantity" => 1
          }
          request(:product_order, :place_order, :body => order, :http_method => :POST).status == 200
        end

        def create_new_global_ipv6
          order = {
              "complexType" => 'SoftLayer_Container_Product_Order_Network_Subnet',
              "packageId" => 0, # everything that's not a Server is package 0 when using placeOrder
              "prices" => [{"id"=>global_ipv6_price_code}],
              "quantity" => 1
          }
          request(:product_order, :place_order, :body => order, :http_method => :POST).status == 200
        end

        def list_networks
          self.list_networks
        end

        private

        ##
        # Queries the SoftLayer API and returns the "category code" required for ordering a Global IPv4 address.
        # @return [Integer]
        def global_ipv4_cat_code
          request(:product_package, '0/get_configuration', :query => 'objectMask=mask[isRequired,itemCategory]').body.map do |item|
            item['itemCategory']['id'] if item['itemCategory']['categoryCode'] == 'global_ipv4'
          end.compact.first
        end

        ##
        # Queries the SoftLayer API and returns the "category code" required for ordering a Global IPv4 address.
        # @return [Integer]
        def global_ipv6_cat_code
          request(:product_package, '0/get_configuration', :query => 'objectMask=mask[isRequired,itemCategory]').body.map do |item|
            item['itemCategory']['id'] if item['itemCategory']['categoryCode'] == 'global_ipv6'
          end.compact.first
        end

        ##
        # Queries the SoftLayer API and returns the "price code" required for ordering a Global IPv4 address.
        # @return [Integer]
        def global_ipv4_price_code
          request(:product_package, '0/get_item_prices', :query => 'objectMask=mask[id,item.description,categories.id]').body.map do |item|
            item['id'] if item['categories'][0]['id'] == global_ipv4_cat_code
          end.compact.first
        end

        ##
        # Queries the SoftLayer API and returns the "price code" required for ordering a Global IPv4 address.
        # @return [Integer]
        def global_ipv6_price_code
          request(:product_package, '0/get_item_prices', :query => 'objectMask=mask[id,item.description,categories.id]').body.map do |item|
            item['id'] if item['categories'][0]['id'] == global_ipv6_cat_code
          end.compact.first
        end

      end
    end
  end
end

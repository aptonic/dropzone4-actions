#
# Author:: Matt Eldridge (<matt.eldridge@us.ibm.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

require 'fog/compute/models/server'

module Fog
  module Compute
    class Softlayer

      class Server < Fog::Compute::Server

        identity  :id,                       :type => :integer
        attribute :name,                     :aliases => 'hostname'
        attribute :domain
        attribute :fqdn,                     :aliases => 'fullyQualifiedDomainName'
        attribute :cpu,                      :aliases => ['startCpus', 'processorCoreAmount']
        attribute :ram,                      :aliases => ['maxMemory', 'memory']
        attribute :disk,                     :aliases => ['blockDevices','hardDrives']
        attribute :private_ip,               :aliases => 'primaryBackendIpAddress'
        attribute :public_ip,                :aliases => 'primaryIpAddress'
        attribute :flavor_id
        attribute :bare_metal,               :type => :boolean
        attribute :os_code
        attribute :image_id
        attribute :ephemeral_storage,        :aliases => 'localDiskFlag'
        attribute :key_pairs,                :aliases => 'sshKeys'

        # Times
        attribute :created_at,              :aliases => ['createDate', 'provisionDate'], :type => :time
        attribute :last_verified_date,      :aliases => 'lastVerifiedDate', :type => :time
        attribute :metric_poll_date,        :aliases => 'metricPollDate', :type => :time
        attribute :modify_date,             :aliases => 'modifyDate', :type => :time

        # Metadata
        attribute :account_id,              :aliases => 'accountId', :type => :integer
        attribute :datacenter,              :aliases => 'datacenter'
        attribute :single_tenant,           :aliases => 'dedicatedAccountHostOnlyFlag'
        attribute :global_identifier,       :aliases => 'globalIdentifier'
        attribute :hourly_billing_flag,     :aliases => 'hourlyBillingFlag'
        attribute :tags,                    :aliases => 'tagReferences'
        attribute :private_network_only,    :aliases => 'privateNetworkOnlyFlag'

        def initialize(attributes = {})
          # Forces every request inject bare_metal parameter
          raise Exception if attributes[:collection].nil? and attributes['bare_metal'].nil?
          super(attributes)
          set_defaults
        end

        def add_tags(tags)
          requires :id
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          tags.each do |tag|
            service.tags.new(:resource_id => self.id, :name => tag).save
          end
          self.reload
          true
        end

        def bare_metal?
          bare_metal
        end
        
        def bare_metal
          @bare_metal
        end

        def datacenter=(name)
          name = name['name'] if name.is_a?(Hash)
          attributes[:datacenter] = { :name => name }
        end

        def datacenter
          attributes[:datacenter][:name] unless attributes[:datacenter].nil?
        end

        def delete_tags(tags)
          requires :id
          raise ArgumentError, "Tags argument for #{self.class.name}##{__method__} must be Array." unless tags.is_a?(Array)
          tags.each do |tag|
            service.tags.new(:resource_id => self.id, :name => tag).destroy
          end
          self.reload
          true
        end

        def destroy
          requires :id
          request = bare_metal? ? :delete_bare_metal_server : :delete_vm
          response = service.send(request, self.id)
          response.body
        end

        def dns_name
          fqdn
        end

        def image_id=(uuid)
          attributes[:image_id] = {:globalIdentifier => uuid}
        end

        def image_id
          attributes[:image_id][:globalIdentifier] unless attributes[:image_id].nil?
        end

        def name=(set)
          attributes[:hostname] = set
        end

        def name
          attributes[:hostname]
        end

        def pre_save
          extract_flavor
          validate_attributes
          if self.vlan
            attributes[:vlan] = { :networkVlan => { :id => self.vlan.id } }
          end
          if self.private_vlan
            attributes[:private_vlan] = { :networkVlan => { :id => self.private_vlan.id } }
          end
          if self.key_pairs
            attributes[:key_pairs].map! { |key| { :id => key.id } }
          end
          remap_attributes(attributes, attributes_mapping)
          clean_attributes
        end

        def os_code
          attributes['operatingSystem']['softwareLicense']['softwareDescription']['referenceCode'] if attributes['operatingSystem']
        end

        def private_vlan
          attributes[:private_vlan] ||= _get_private_vlan
        end

        def private_vlan=(value)
          unless value.is_a?(Integer) or value.is_a?(Fog::Network::Softlayer::Network)
            raise ArgumentError, "vlan argument for #{self.class.name}##{__method__} must be Integer or Fog::Network::Softlayer::Network."
          end
          value = Fog::Network[:softlayer].networks.get(value) if value.is_a?(Integer)
          attributes[:private_vlan] = value
        end

        def key_pairs
          attributes[:key_pairs]
        end

        def key_pairs=(keys)
          raise ArgumentError, "Argument #{local_variables.first.to_s} for #{self.class.name}##{__method__} must be Array." unless keys.is_a?(Array)
          attributes[:key_pairs] = []
          keys.map do |key|
            key = self.symbolize_keys(key) if key.is_a?(Hash)
            unless key.is_a?(Fog::Compute::Softlayer::KeyPair) or (key.is_a?(Hash) and key[:id])
              raise ArgumentError, "Elements of keys array for #{self.class.name}##{__method__} must be a Hash with key 'id', or Fog::Compute::Softlayer::KeyPair"
            end
            key = service.key_pairs.get(key[:id]) unless key.is_a?(Fog::Compute::Softlayer::KeyPair)
            attributes[:key_pairs] << key
          end
        end

        def vlan
          attributes[:vlan] ||= _get_vlan
        end

        def vlan=(value)
          unless value.is_a?(Integer) or value.is_a?(Fog::Network::Softlayer::Network)
            raise ArgumentError, "vlan argument for #{self.class.name}##{__method__} must be Integer or Fog::Network::Softlayer::Network."
          end
          value = Fog::Network[:softlayer].networks.get(value) if value.is_a?(Integer)
          attributes[:vlan] = value
        end

        def ram=(set)
          if set.is_a?(Array) and set.first['hardwareComponentModel']
            set = 1024 * set.first['hardwareComponentModel']['capacity'].to_i
          end
          attributes[:ram] = set
        end

        def ready?
          if bare_metal?
            state == "on"
          else
            state == "Running"
          end
        end

        def reboot(use_hard_reboot = true)
          # TODO: implement
        end

        def ssh_password
          self.os['passwords'][0]['password'] if self.id
        end

        def snapshot
          # TODO: implement
        end

        def start
          # TODO: implement

          #requires :identity
          #service.start_server(identity)
          true
        end

        def stop
          # TODO: implement
        end

        def shutdown
          # TODO: implement
        end

        def state
          if bare_metal?
            service.request(:hardware_server, "#{id}/getServerPowerState").body
          else
            service.request(:virtual_guest, "#{id}/getPowerState").body['name']
          end
        end

        # Creates server
        # * requires attributes: :name, :domain, and :flavor_id OR (:cpu_count && :ram && :disks)
        #
        # @note You should use servers.create to create servers instead calling this method directly
        #
        # * State Transitions
        #   * BUILD -> ACTIVE
        #   * BUILD -> ERROR (on error)
        def save
          raise Fog::Errors::Error.new('Resaving an existing object may create a duplicate') if persisted?
          copy = self.dup
          copy.pre_save

          data = if bare_metal?
            service.create_bare_metal_server(copy.attributes).body
          else
            service.create_vm(copy.attributes).body.first
          end

          data.delete("bare_metal")
          merge_attributes(data)
          true
        end

        def tags
          attributes[:tags].map { |i| i['tag']['name'] } if attributes[:tags]
        end

        private

        def _get_private_vlan
          if self.id
            vlan_id = if bare_metal?
              service.request(:hardware_server, "#{self.id}/get_private_vlan").body['id']
            else
              service.request(:virtual_guest, self.id, :query => 'objectMask=primaryBackendNetworkComponent.networkVlan').body['primaryBackendNetworkComponent']['networkVlan']['id']
            end
            Fog::Network[:softlayer].networks.get(vlan_id)
          end
        end

        def _get_vlan
          if self.id
            vlan_id = if bare_metal?
              service.request(:hardware_server, "#{self.id}/get_public_vlan").body['id']
            else
              service.request(:virtual_guest, self.id, :query => 'objectMask=primaryNetworkComponent.networkVlan').body['primaryNetworkComponent']['networkVlan']['id']
            end
            Fog::Network[:softlayer].networks.get(vlan_id)
          end
        end

        ##
        # Generate mapping for use with remap_attributes
        def attributes_mapping
          common = {
              :hourly_billing_flag => :hourlyBillingFlag,
              :os_code  =>  :operatingSystemReferenceCode,
              :vlan => :primaryNetworkComponent,
              :private_vlan => :primaryBackendNetworkComponent,
              :key_pairs => :sshKeys,
              :private_network_only => :privateNetworkOnlyFlag,

          }

          conditional = if bare_metal?
            {
              :cpu  =>   :processorCoreAmount,
              :ram  =>   :memoryCapacity,
              :disk =>   :hardDrives,
              :bare_metal => :bareMetalInstanceFlag
            }
          else
            {
              :cpu  =>   :startCpus,
              :ram  =>   :maxMemory,
              :disk =>   :blockDevices,
              :image_id =>  :blockDeviceTemplateGroup,
              :ephemeral_storage => :localDiskFlag,
            }
          end
          common.merge(conditional)
        end

        def bare_metal=(set)
          raise Exception, "Bare metal flag has already been set" unless @bare_metal.nil?
          @bare_metal = case set
            when false, 'false', 0, nil, ''
              false
            else
              true
          end
        end
        
        ##
        # Remove model attributes that aren't expected by the SoftLayer API
        def clean_attributes
          attributes.delete(:bare_metal)
          attributes.delete(:flavor_id)
          attributes.delete(:ephemeral_storage)
        end


        ##
        # Expand a "flavor" into cpu, ram, and disk attributes
        def extract_flavor
          if attributes[:flavor_id]
            flavor = @service.flavors.get(attributes[:flavor_id])
            flavor.nil? and Fog::Errors::Error.new("Unrecognized flavor in #{self.class}##{__method__}")
            attributes[:cpu] = flavor.cpu
            attributes[:ram] = flavor.ram
            attributes[:disk] = flavor.disk unless attributes[:image_id]
            if bare_metal?
              value = flavor.disk.first['diskImage']['capacity'] < 500 ? 250 : 500
              attributes[:disk] = [{'capacity'=>value}]
              attributes[:ram] = attributes[:ram] / 1024 if attributes[:ram] > 64
            end
          end
        end

        def validate_attributes
          requires :name, :domain, :cpu, :ram, :datacenter
          requires_one :os_code, :image_id
          requires_one :image_id, :disk
          bare_metal? and image_id and raise ArgumentError, "Bare Metal Cloud does not support booting from Image"
        end

        def set_defaults
          attributes[:hourly_billing_flag] = true if attributes[:hourly_billing_flag].nil?
          attributes[:ephemeral_storage] = false if attributes[:ephemeral_storage].nil?
          attributes[:domain] = service.softlayer_default_domain if service.softlayer_default_domain and attributes[:domain].nil?
          self.datacenter = service.softlayer_default_datacenter if service.softlayer_default_datacenter and attributes[:datacenter].nil?
        end

      end
    end
  end
end

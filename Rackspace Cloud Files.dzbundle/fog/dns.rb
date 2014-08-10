module Fog
  module DNS

    def self.[](provider)
      self.new(:provider => provider)
    end

    def self.new(attributes)
      attributes = attributes.dup # prevent delete from having side effects
      case provider = attributes.delete(:provider).to_s.downcase.to_sym
      when :stormondemand
        require 'fog/storm_on_demand/dns'
        Fog::DNS::StormOnDemand.new(attributes)
      else
        if self.providers.include?(provider)
          require "fog/#{provider}/dns"
          begin
            Fog::DNS.const_get(Fog.providers[provider])
          rescue
            Fog::const_get(Fog.providers[provider])::DNS
          end.new(attributes)
        else
          raise ArgumentError.new("#{provider} is not a recognized dns provider")
        end
      end
    end

    def self.providers
      Fog.services[:dns]
    end

    def self.zones
      zones = []
      for provider in self.providers
        begin
          zones.concat(self[provider].zones)
        rescue # ignore any missing credentials/etc
        end
      end
      zones
    end

  end
end

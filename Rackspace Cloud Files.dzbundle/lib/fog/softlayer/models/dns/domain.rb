#
# Author:: Celso Fernandes (<fernandes@zertico.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/model'
require 'fog/softlayer/models/dns/records'

module Fog
  module DNS
    class Softlayer

      class Domain < Fog::Model

        identity  :id,           :type => :integer
        attribute :name,         :aliases => 'domain'
        attribute :serial,       :type => :integer
        
        # Times
        attribute :updated_at,   :aliases => 'updateDate', :type => :time

        def initialize(attributes = {})
          super(attributes)
        end
        
        def records(reload = false)
          @records = nil if reload
          @records ||= begin
            Fog::DNS::Softlayer::Records.new(
              :domain       => self,
              :service      => service
            )
          end
        end
        
        def create_record(opts = {})
          opts.merge!({:domain_id => self.id, :service => service})
          record = Fog::DNS::Softlayer::Record.new(opts)
          record.save
          records(true)
          record
        end
        
        def destroy
          requires :id
          response = service.delete_domain self.id
          response.body
        end
      end
    end
  end
end

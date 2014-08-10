#
# Author:: Celso Fernandes (<fernandes@zertico.com>)
# © Copyright IBM Corporation 2014.
#
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
require 'fog/core/model'

module Fog
  module DNS
    class Softlayer
      class Record < Fog::Model
        identity  :id
        attribute :domain_id,     :aliases => "domainId"
        attribute :name,          :aliases => "host"
        attribute :value,         :aliases => "data"
        attribute :ttl
        attribute :priority,      :aliases => "mxPriority"
        attribute :type
        attribute :expire
        attribute :minimum
        attribute :refresh
        attribute :retry
         
        def initialize(attributes={})
          self.domain_id = attributes[:domain_id]
          super(attributes)
        end

        def destroy
          response = service.delete_record(identity)
          response.body
        end

        def save
          requires :name, :type, :value, :domain_id
          opts = generate_template

          # to save or to update, thats the question
          if id.nil?
            data = service.create_record(opts)
            merge_attributes(data.body)
          else
            data = service.update_record(self.id, opts)
          end
          true
        end

        private
        def generate_template
          template = {}
          template[:host] = self.name
          template[:data] = self.value
          template[:type] = self.type
          template[:domainId] = self.domain_id

          template[:ttl] = self.ttl if self.ttl
          template[:mxPriority] = self.priority if self.priority
          template[:expire] = self.expire if self.expire
          template[:minimum] = self.minimum if self.minimum
          template[:refresh] = self.refresh if self.refresh
          template[:retry] = self.retry if self.retry
          template
        end
      end
    end
  end
end
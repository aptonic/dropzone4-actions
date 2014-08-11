require "fog/brightbox/model"

module Fog
  module Compute
    class Brightbox
      # @api private
      class Event < Fog::Brightbox::Model

        identity :id
        attribute :url
        attribute :resource_type

        attribute :action
        attribute :message
        attribute :short_message

        # Times
        attribute :created_at, :type => :time

        # Links - to be replaced
        attribute :resource
        attribute :client
        attribute :user

      end
    end
  end
end

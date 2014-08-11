require "fog/brightbox/model"

module Fog
  module Compute
    class Brightbox
      class Zone < Fog::Brightbox::Model
        identity :id
        attribute :url
        attribute :resource_type

        attribute :status
        attribute :handle

        attribute :description
      end
    end
  end
end
